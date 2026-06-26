# Lanhu MCP installation for xz01 workflow

Use when the user asks how to install or connect `https://github.com/dsphper/lanhu-mcp` for the xz01/Hermes+Claude workflow.

## Recommendation

Prefer this architecture:

```text
Lanhu MCP server = Docker Compose HTTP service
Hermes = native MCP HTTP client
Claude Code = HTTP MCP client pointed at the same service
/root/.openclaw = read-only learning corpus; do not install or configure Lanhu there
```

Recommended install directory:

```text
/root/.hermes/workspace/lanhu-mcp
```

Rationale:

- `lanhu-mcp` is a long-running HTTP MCP server (`/mcp`), not a one-shot stdio/npx tool.
- It depends on Python + Playwright/Chromium; Docker isolates those dependencies from Hermes and Claude.
- It requires `LANHU_COOKIE`, so keeping secrets in the service `.env` is clearer than mixing them into unrelated configs.
- Hermes, Claude dev, Hermes test, and Hermes rule can share one service with different URL query parameters.

## Install outline

```bash
mkdir -p /root/.hermes/workspace
git clone https://github.com/dsphper/lanhu-mcp.git /root/.hermes/workspace/lanhu-mcp
cd /root/.hermes/workspace/lanhu-mcp
cp config.example.env .env
# edit .env and set LANHU_COOKIE; optionally FEISHU_WEBHOOK_URL
# keep SERVER_HOST=0.0.0.0 and SERVER_PORT=8000 unless there is a port conflict
docker compose up -d --build
```

Verify:

```bash
docker compose ps
docker compose logs --tail=100 lanhu-mcp
curl http://127.0.0.1:8000/health
```

MCP endpoint pattern:

```text
http://127.0.0.1:8000/mcp?role=Developer&name=HermesMain
```

Use English URL parameter values; some clients do not handle Chinese query parameters reliably.

## Hermes native MCP config

Hermes needs the Python MCP package available in its environment:

```bash
pip install mcp
```

Then configure Hermes `mcp_servers`:

```yaml
mcp_servers:
  lanhu:
    url: "http://127.0.0.1:8000/mcp?role=Developer&name=HermesMain"
    timeout: 180
    connect_timeout: 60
```

Restart Hermes after changing MCP config; MCP tools are discovered on startup. Expected tool names are prefixed like:

```text
mcp_lanhu_lanhu_get_pages
mcp_lanhu_lanhu_get_designs
mcp_lanhu_lanhu_get_ai_analyze_page_result
mcp_lanhu_lanhu_get_ai_analyze_design_result
```

## Claude Code config

Point Claude Code to the same HTTP service, with a separate identity:

```json
{
  "mcpServers": {
    "lanhu": {
      "type": "http",
      "url": "http://127.0.0.1:8000/mcp?role=Developer&name=ClaudeDev"
    }
  }
}
```

Suggested identities:

| Role | URL suffix |
|---|---|
| Hermes main | `?role=Developer&name=HermesMain` |
| Claude dev | `?role=Developer&name=ClaudeDev` |
| Hermes test | `?role=Tester&name=HermesTest` |
| Hermes rule | `?role=Developer&name=HermesRule` |

## Required secret

`LANHU_COOKIE` is required. Do not guess it or search for it in unrelated files. The user must provide it or obtain it from a logged-in Lanhu browser session.

## Pitfalls

- Do not install this under `/root/.openclaw`; that tree is read-only for this workflow.
- Do not use stdio/npx as the primary integration; this project is designed to run as an HTTP MCP service.
- Do not expose the service publicly without access control; Lanhu cookies and cached design data are sensitive.
- Do not treat failure before `LANHU_COOKIE` is configured as a durable tool failure; it is a missing credential/setup state.
