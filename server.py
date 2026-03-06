import ast
import math
import operator
import sys

class _FlushWriter:
    def __init__(self, stream):
        self._s = stream
    def write(self, data):
        self._s.write(data)
        self._s.flush()
    def __getattr__(self, name):
        return getattr(self._s, name)

if not sys.stdout.isatty():
    sys.stdout = _FlushWriter(sys.stdout)

from fastmcp import FastMCP

mcp = FastMCP(name="mcp-server")

# --- Safe eval for calculate tool ---
_SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}
_SAFE_NAMES = {
    "abs": abs, "round": round, "sqrt": math.sqrt,
    "ceil": math.ceil, "floor": math.floor,
    "pi": math.pi, "e": math.e,
    "log": math.log, "log10": math.log10,
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
}


def _safe_eval(node):
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant: {type(node.value)}")
    if isinstance(node, ast.Name):
        if node.id in _SAFE_NAMES:
            return _SAFE_NAMES[node.id]
        raise ValueError(f"Unknown name: {node.id!r}")
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _SAFE_OPS:
            raise ValueError(f"Unsupported operator")
        return _SAFE_OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _SAFE_OPS:
            raise ValueError(f"Unsupported unary operator")
        return _SAFE_OPS[type(node.op)](_safe_eval(node.operand))
    if isinstance(node, ast.Call):
        func = _safe_eval(node.func)
        if not callable(func):
            raise ValueError("Not callable")
        return func(*[_safe_eval(a) for a in node.args])
    raise ValueError(f"Unsupported node: {type(node).__name__}")


# --- Tool: evaluate a math expression ---
@mcp.tool
def calculate(expression: str) -> str:
    """Evaluate a math expression. Supports +, -, *, /, **, %, // and functions like sqrt, sin, cos, pi, e."""
    try:
        tree = ast.parse(expression.strip(), mode="eval")
        result = _safe_eval(tree)
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)
    except ZeroDivisionError:
        return "Error: division by zero"
    except Exception as e:
        return f"Error: {e}"


# --- Resource: server info ---
@mcp.resource("app://info")
def get_info() -> dict:
    """Server name and capabilities."""
    return {"name": "mcp-server", "capabilities": ["calculate", "prompts", "resources"]}


# --- Prompt: ask to explain a topic ---
@mcp.prompt
def explain(topic: str) -> str:
    """Ask the model to explain a topic clearly."""
    return f"Please explain the following in simple terms: {topic}"


if __name__ == "__main__":
    mcp.run()
