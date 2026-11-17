# MCP setup and tool mapping

Targets Scrapling >=0.5,<0.6. The authoritative definitions are the installed
server's live schemas and the [official MCP guide](https://scrapling.readthedocs.io/en/latest/ai/mcp-server.html).

## Installation and registration

```sh
python -m pip install "scrapling[ai]>=0.5,<0.6"
scrapling install
```

Install the separate `mcporter` CLI if it is not present. Its
[configuration reference](https://github.com/openclaw/mcporter/blob/main/docs/config.md)
describes supported config sources; this is mcporter configuration, not a
claim that every OpenClaw version reads `mcpServers` directly.

Example `config/mcporter.json`, relative to the workspace invoking mcporter:

```json
{
  "mcpServers": {
    "scrapling": {
      "command": "python",
      "args": ["-X", "utf8", "-c", "from scrapling.cli import mcp; mcp()"],
      "lifecycle": "keep-alive"
    }
  }
}
```

The Python snippet calls the official `scrapling.cli:mcp` entrypoint. Use the
absolute virtual-environment Python path when the caller has a different PATH.
Direct `"command": "scrapling-mcp"`, `"args": []`, or `"command": "scrapling"`,
`"args": ["mcp"]`, are alternatives when the runner supports those launchers.
In a Windows mcporter 0.16.1 check, the `.exe` launcher closed the connection;
calling the entrypoint with Python worked. Resolve the environment's Python
instead of adding manual PYTHONPATH overrides. Neither `scrapling.mcp` nor
`python -m scrapling.cli mcp` is a working module entrypoint in 0.5.

```sh
mcporter list scrapling --schema
mcporter list scrapling --all-parameters
```

Always inspect schemas after an upgrade. Commands below use mcporter's
`server.tool` syntax, with JSON arguments for nested options. On PowerShell,
use a version that preserves native-command JSON quoting, or use the equivalent
named arguments for simple calls.

## Current tool families

| Tools | Purpose |
| --- | --- |
| `make_request`, `browser_fetch_once` | One URL, automatically closed HTTP/browser resources |
| `open_request_session`, `session_make_request` | Reusable HTTP session |
| `browser_open`, `browser_fetch` | Reusable browser and navigation |
| `browser_extract`, `browser_actions`, `browser_evaluate` | Read/interact with the current page |
| `browser_screenshot` | Capture the current page or an element without navigation |
| `browser_network_requests`, `browser_network_request` | Inspect captured network history |
| `browser_save_state`, `browser_load_state` | Save/restore authenticated browser state on the server machine |
| `list_sessions`, `close_session` | Inspect and release persistent resources |

There are no standalone `css_select`, `xpath_select`, adaptive-selector or
`start_spider` tools. CSS narrowing is part of fetch/conversion; use Python
for XPath, adaptive storage or a full Spider.

## HTTP request

```sh
mcporter call scrapling.make_request --args '{"url":"https://example.com","extraction_type":"text","css_selector":"h1","timeout":30,"retries":3,"retry_delay":1}'
```

`timeout` and `retry_delay` are seconds. `retries` is the maximum number of
attempts including the first. There is no general `delay` argument. Control
spacing between pages in the caller or Spider.

`main_content_only=true` cleans the body before selecting. For `<title>`, meta
or other head content, explicitly set it false. Fetch results contain `status`,
`url`, and `content` as a list of strings. Check both status and content.

## Browser fetch

```sh
mcporter call scrapling.browser_fetch_once --args '{"url":"https://example.com","headless":true,"wait_selector":"h1","timeout":30000,"extraction_type":"text","css_selector":"h1"}'
```

Use `wait_selector`, not `wait_for`; browser timeout/wait values are milliseconds.
Set `solve_cloudflare=true` when needed; it is not a guarantee. Resource blocking
can break rendering, so enable `disable_resources` only for suitable targets.

## Persistent sessions

Example sequence; replace `YOUR_SESSION_ID` with the ID actually returned:

The config above selects `lifecycle: "keep-alive"` so mcporter can retain the
stdio server through its daemon. Start/check the daemon before multi-call work;
`"ephemeral"` is suitable for standalone fetches, not cross-process sessions.

```sh
mcporter daemon start
mcporter call scrapling.browser_open headless:true
mcporter call scrapling.browser_fetch session_id:YOUR_SESSION_ID url:https://example.com
mcporter call scrapling.browser_extract session_id:YOUR_SESSION_ID extraction_type:snapshot
mcporter call scrapling.close_session session_id:YOUR_SESSION_ID
```

Session creation returns `session_id` and `session_type`; inspect settings with
`list_sessions`. Session-level options such as headless/proxy are set at open;
request-level waits, selectors and Cloudflare solving belong on each fetch.
Use `open_request_session` plus `session_make_request` for HTTP reuse instead.

After inspecting a snapshot, build `browser_actions` from the live action
schema. Do not infer page references or action payloads. Use `browser_extract`
to read changed content without refetching; its element parameter is `target`,
whereas fetch tools use `css_selector`. Close persistent sessions on success,
failure and cancellation. With mcporter, verify session reuse across processes
using its persistent daemon (`mcporter daemon --help`) and the configured
keep-alive lifecycle; do not assume separate short-lived CLI
processes share in-memory sessions. One-shot fetch tools need no persistent
client connection.

Saved browser state can contain login secrets; files live on the MCP server's
machine. Do not commit them. Inspect only authorized network responses and
redact credentials from any exported evidence.

## Remote transport

Prefer local stdio for a local agent. If an existing deployment requires HTTP,
use the official server's authentication and host controls; for example:

```sh
scrapling-mcp --http
```

For authenticated HTTP, provide `SCRAPLING_MCP_AUTH_TOKEN` through the process's
secure environment and configure the matching Bearer header in the client.
HTTP without authentication is refused unless explicitly started with
`--no-auth`. Do not expose an unauthenticated listener publicly; use TLS and
appropriate `--allowed-host` values for a remote deployment. Setting up a
remote service is separate from installing this guidance skill.
