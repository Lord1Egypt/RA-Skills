---
name: mcp-forge
description: "MCP (Model Context Protocol) server builder — guides creation of high-quality MCP servers in Python (FastMCP) or TypeScript (MCP SDK). Use when building integrations for AI agents."
metadata: { "openclaw": { "emoji": "🔌", "homepage": "https://clawhub.ai/NakedoShadow", "requires": { "anyBins": ["node", "python", "python3", "uv"] }, "os": ["darwin", "linux", "win32"] } }
---

# MCP Forge — Model Context Protocol Server Builder

**Version**: 1.1.0 | **Author**: Shadows Company | **License**: MIT

---

## WHEN TO TRIGGER

- User wants to create an MCP server
- Integrating an external API/service with AI agents
- User says "build MCP", "create a tool server", "MCP server"
- Connecting a database, API, or service to Claude/OpenClaw

## WHEN NOT TO TRIGGER

- Using existing MCP servers (just configure them)
- Building regular REST APIs (use standard web framework)

## PREREQUISITES

Requires at least one of: `python`/`python3`/`uv` (for Python MCP servers) or `node` (for TypeScript MCP servers). The skill auto-detects the user's preferred stack based on available binaries.

- **Python path**: Requires `fastmcp` package (`pip install fastmcp`). Optional: `httpx` for HTTP clients, `pytest` for testing.
- **TypeScript path**: Requires `@modelcontextprotocol/sdk` and `zod` packages (`npm install`). Optional: `tsx` for development.
- **uv path**: Can replace pip/python with `uv run` for faster setup.

Additional tooling (`pip`, `npm`) is used only for dependency installation when explicitly requested by the user.

---

## QUICK DECISION: PYTHON OR TYPESCRIPT?

| Factor | Python (FastMCP) | TypeScript (MCP SDK) |
|--------|------------------|---------------------|
| Speed to build | Faster (less boilerplate) | More setup |
| Type safety | Runtime checks | Compile-time checks |
| Ecosystem | Data/ML/scripting | Web/Node ecosystem |
| Hosting | uvx, pip | npx, npm |

**Default**: Python with FastMCP unless the user needs TypeScript.

---

## PYTHON — FastMCP Template

### Minimal Server

```python
from fastmcp import FastMCP

mcp = FastMCP("my-service", description="What this server does")

@mcp.tool()
async def my_tool(param: str) -> str:
    """Description of what this tool does.

    Args:
        param: Description of the parameter
    """
    # Implementation here
    return f"Result for {param}"

@mcp.resource("resource://{name}")
async def get_resource(name: str) -> str:
    """Fetch a named resource."""
    return f"Content of {name}"
```

### Project Structure

```
my-mcp-server/
  __init__.py
  server.py          # FastMCP instance + tools
  config.py          # Environment variables, constants
  requirements.txt   # fastmcp, httpx, etc.
  README.md          # Usage instructions
```

### Running

```bash
# Development
fastmcp dev server.py

# Install in Claude/OpenClaw
fastmcp install server.py --name "My Service"

# Or configure manually in settings
```

---

## TYPESCRIPT — MCP SDK Template

### Minimal Server

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-service",
  version: "1.0.0",
});

server.tool(
  "my-tool",
  "Description of what this tool does",
  { param: z.string().describe("Description of param") },
  async ({ param }) => ({
    content: [{ type: "text", text: `Result for ${param}` }],
  })
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

### Project Structure

```
my-mcp-server/
  src/
    index.ts        # McpServer instance + tools
    config.ts       # Environment variables
  package.json      # @modelcontextprotocol/sdk, zod
  tsconfig.json
  README.md
```

---

## DESIGN PRINCIPLES

### 1. Tool Design

- **One tool = one action** — do not create god tools that handle multiple unrelated operations
- **Clear names** — `get_user`, `create_issue`, not `do_thing`
- **Descriptive parameters** — use docstrings/descriptions for every param
- **Return structured data** — JSON-serializable results
- **Error handling** — return error messages in the response, never let the server crash

### 2. Security

- **Never hardcode secrets** — use environment variables via `os.environ` or `process.env`
- **Validate inputs** — check types, ranges, formats at every tool boundary
- **Sanitize outputs** — strip internal paths, stack traces, and system details from responses
- **Rate limiting** — protect against runaway agent loops with request throttling
- **Principle of least privilege** — only request the permissions the tool actually needs

### 3. Performance

- **Async by default** — use `async/await` for all I/O operations
- **Connection pooling** — reuse HTTP clients and DB connections across tool calls
- **Timeouts** — set explicit timeouts (e.g., 30s) on all external calls
- **Caching** — cache frequently-accessed, rarely-changing data with TTL

### 4. Testing

```python
# Python testing with FastMCP
import pytest
from fastmcp import Client

@pytest.fixture
def client():
    return Client(mcp)

@pytest.mark.asyncio
async def test_my_tool(client):
    result = await client.call_tool("my_tool", {"param": "test"})
    assert "Result" in result.text
```

---

## CONFIGURATION FORMAT

For OpenClaw/Claude Desktop:
```json
{
  "mcpServers": {
    "my-service": {
      "command": "python",
      "args": ["-m", "my_mcp_server.server"],
      "env": {
        "API_KEY": "from-env-or-secrets"
      }
    }
  }
}
```

---

## SECURITY CONSIDERATIONS

This skill generates new source code files (scaffolding MCP servers). It does NOT execute the generated code during scaffolding.

- **Commands suggested**: `pip install fastmcp`, `npm install @modelcontextprotocol/sdk` — these install packages from public registries. Review package names before running.
- **Data read**: The skill reads the user's project structure to determine stack preferences. No sensitive files are accessed.
- **Network access**: None from the skill itself. Generated servers may make network calls depending on their purpose — this is by design and documented per-server.
- **Credentials**: The skill explicitly instructs to use environment variables for secrets and never hardcode credentials in source files.
- **Persistence**: Generated files are written to the working directory only. No global config changes.
- **Sandboxing**: Recommended to run generated MCP servers in isolated environments (containers, venvs) during development.

---

## RULES

1. **One purpose per server** — do not mix unrelated tools in a single server
2. **Document every tool** — description + parameter docs are mandatory for each tool
3. **Environment variables for secrets** — never hardcode API keys or tokens
4. **Test before publishing** — verify all tools work with a client before distribution
5. **README is mandatory** — every server must include installation, configuration, and usage examples

---

**Published by Shadows Company — "We work in the shadows to serve the Light."**
