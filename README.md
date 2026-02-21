# MCP Server 
## Developed with Claude Code

A minimal [Model Context Protocol](https://modelcontextprotocol.io) server written in Python, with two example tools:

| Tool | Description |
|------|-------------|
| `get_weather` | Live weather for any city (powered by [wttr.in](https://wttr.in) — no API key needed) |
| `calculate` | Safe evaluation of math expressions (`sqrt`, `sin`, `pi`, `**`, …) |

---

## Requirements

- Python 3.10+
- pip

---

## Setup

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

MCP servers communicate over **stdio**, so you normally don't run the server directly — your MCP client launches it. See the client configuration section below.

To verify the server starts without errors:

```bash
python server.py
# The process will block waiting for MCP messages — that's expected.
# Press Ctrl+C to quit.
```

---

## Connecting to Claude Desktop

Add the server to Claude Desktop's config file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "example-server": {
      "command": "/absolute/path/to/MCP-Server/.venv/bin/python",
      "args": ["/absolute/path/to/MCP-Server/server.py"]
    }
  }
}
```

Replace the paths with the actual absolute paths on your machine. Restart Claude Desktop after saving.

---

## Connecting via Claude Code (CLI)

```bash
claude mcp add example-server \
  /absolute/path/to/MCP-Server/.venv/bin/python \
  -- /absolute/path/to/MCP-Server/server.py
```

---

## Tool reference

### `get_weather`

```
Input:  { "city": "Tokyo" }
Output: Weather for Tokyo, Japan:
          Condition : Partly cloudy
          Temp      : 18°C / 64°F
          Feels like: 17°C
          Humidity  : 60%
          Wind      : 15 km/h NE
```

### `calculate`

Supported operators: `+`, `-`, `*`, `/`, `**`, `%`, `//`

Supported functions: `abs`, `round`, `sqrt`, `ceil`, `floor`, `log`, `log10`, `sin`, `cos`, `tan`

Constants: `pi`, `e`

```
Input:  { "expression": "sqrt(2) * pi" }
Output: 4.442882938158366

Input:  { "expression": "2 ** 10" }
Output: 1024
```

---

## Project structure

```
MCP-Server/
├── server.py          # MCP server with tool implementations
├── requirements.txt   # Python dependencies
└── README.md
```

---

## Extending the server

To add a new tool:

1. Add a `types.Tool(...)` entry inside `handle_list_tools()`.
2. Add a matching `elif name == "your_tool":` branch inside `handle_call_tool()`.
3. Implement the tool logic as a plain function (sync) or `async` coroutine.
