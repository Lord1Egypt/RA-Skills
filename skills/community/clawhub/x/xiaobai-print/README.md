# xiaobai-print

This repository now centers on the wrapper-skill flow:

1. Run a local HTTP bridge
2. Read the bridge tool list
3. Generate one or more OpenClaw skill directories
4. Let each skill call the bridge through a local `invoke.js`

The repository still includes the stdio MCP server for Claude Desktop / Cursor, but the recommended OpenClaw path is:

`OpenClaw skill -> scripts/invoke.js -> local HTTP bridge -> remote MCP`

## Build

```bash
npm install
npm run build
```

## Executables

- `xiaobai-print-mcp`: stdio MCP server
- `xiaobai-print-bridge`: local HTTP bridge for generated skills
- `generate-openclaw-skill`: skill generator that reads the bridge tool list

## Run The Local Bridge

Start the local HTTP bridge on `127.0.0.1:8787`:

```bash
MY_MCP_UPSTREAM_URL="https://mcp.gongfudou.com/mcp/openclaw/sse" \
MY_MCP_TOKEN="your-token" \
xiaobai-print-bridge
```

Or use the compiled file directly:

```bash
node dist/bridge/http.js --host 127.0.0.1 --port 8787
```

Bridge endpoints:

- `GET /health`
- `GET /mcp/tools`
- `POST /mcp/tools/{toolName}`

The bridge accepts `Authorization: Bearer <token>` per request. If the request omits `Authorization`, it falls back to `MY_MCP_TOKEN` / `OPENCLAW_TOKEN`.

## Generate OpenClaw Skills

Generate a single skill from the local bridge:

```bash
generate-openclaw-skill \
  --bridge-url http://127.0.0.1:8787 \
  --out ./skill \
  --skill-name my-mcp
```

Split tools into multiple skill directories by tool-name prefix:

```bash
generate-openclaw-skill \
  --bridge-url http://127.0.0.1:8787 \
  --out ./skills \
  --skill-name my-mcp \
  --split-by prefix
```

Optional discovery auth:

```bash
generate-openclaw-skill \
  --bridge-url http://127.0.0.1:8787 \
  --out ./skill \
  --token "$MY_MCP_TOKEN"
```

Generated output for a single skill:

```text
skill/
  SKILL.md
  scripts/
    invoke.js
  schema/
    tools.json
```

Generated output for `--split-by prefix`:

```text
skills/
  schema/
    tools.json
  my-mcp-search/
    SKILL.md
    scripts/
      invoke.js
    schema/
      tools.json
  my-mcp-ticket/
    ...
```

The generated wrapper uses:

- `MY_MCP_TOKEN` for the bearer token
- `MY_MCP_BASE_URL` for the local bridge URL

If `MY_MCP_BASE_URL` is not set, the wrapper falls back to the bridge URL used during generation.

## OpenClaw Configuration

Recommended skill configuration:

```json
{
  "skills": {
    "entries": {
      "my-mcp": {
        "enabled": true,
        "apiKey": "your-token-here",
        "env": {
          "MY_MCP_BASE_URL": "http://127.0.0.1:8787"
        }
      }
    }
  }
}
```

The generated `SKILL.md` declares:

- `metadata.openclaw.requires.env = ["MY_MCP_TOKEN"]`
- `metadata.openclaw.primaryEnv = "MY_MCP_TOKEN"`

That lets OpenClaw inject `skills.entries.<skill>.apiKey` as `MY_MCP_TOKEN`.

## MCP Server Mode

The original stdio MCP server is still available:

```bash
node dist/index.js
```

Environment variables:

| Variable | Required | Description |
| --- | --- | --- |
| `MY_MCP_TOKEN` or `OPENCLAW_TOKEN` | Yes | Bearer token for the upstream remote MCP |
| `MY_MCP_UPSTREAM_URL` or `OPENCLAW_MCP_URL` | No | Upstream remote MCP endpoint URL |

## Examples

A checked-in generated example lives in `examples/search-docs-skill/`.

The bundled print skill now also follows the wrapper-based layout:

```text
skills/xiaobai-print/
  SKILL.md
  scripts/
    invoke.js
  schema/
    tools.json
```
