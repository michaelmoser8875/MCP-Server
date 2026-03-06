# MCP Server (FastMCP)

A minimal [Model Context Protocol](https://modelcontextprotocol.io) server using [FastMCP](https://gofastmcp.com), with one tool, one prompt, and one resource.

| Type     | Name        | Description |
|----------|-------------|-------------|
| **Tool** | `calculate` | Safe math expression evaluation (`sqrt`, `sin`, `pi`, etc.) |
| **Prompt** | `explain` | Ask the model to explain a topic in simple terms |
| **Resource** | `app://info` | Server name and capabilities (read-only) |

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

MCP servers use **stdio** by default. Your MCP client launches the process. To verify it starts:

```bash
python server.py
# Blocks waiting for MCP messages. Press Ctrl+C to quit.
```

---

## Connecting to Claude Desktop

Add to your Claude Desktop config:

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

Use your actual paths and restart Claude Desktop.

---

## Using with MCP Dashboard

The MCP Dashboard launches this server as a subprocess and talks to it over stdio, so tools, resources, and prompts all appear in the UI.

From the MCP-Dashboard directory (with Flask installed), run:

```bash
# Unbuffered (-u) so the dashboard receives list responses immediately
python app.py -- python -u path/to/MCP-Server/server.py
```

Windows:

```bash
python app.py -- python -u path\to\MCP-Server\server.py
```

Use a Python that has both `flask` and `fastmcp` installed (or use the full path to this repo's venv Python if you use one).

The dashboard will open at http://localhost:8080 and show the **calculate** tool, **app://info** resource, and **explain** prompt. You can try the tool, read the resource, and get the prompt from the browser.

---

## Reference

### Tool: `calculate`

- **Input:** `{ "expression": "sqrt(2) * pi" }`
- **Output:** `"4.442882938158366"`
- Supports: `+`, `-`, `*`, `/`, `**`, `%`, `//`, and functions like `abs`, `round`, `sqrt`, `ceil`, `floor`, `log`, `log10`, `sin`, `cos`, `tan`; constants `pi`, `e`.

### Prompt: `explain`

- **Input:** `{ "topic": "recursion" }`
- Returns a user message asking the model to explain the topic in simple terms.

### Resource: `app://info`

- Read-only. Returns JSON: `{"name": "mcp-server", "capabilities": ["calculate", "prompts", "resources"]}`.

---

## Project structure

```
MCP-Server/
├── server.py
├── requirements.txt
└── README.md
```

To add more tools, prompts, or resources, use the `@mcp.tool`, `@mcp.prompt`, and `@mcp.resource(...)` decorators in `server.py`.
