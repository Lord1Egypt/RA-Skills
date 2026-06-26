# Proxy and OpenAPI

Use this reference when the user wants to expose an existing HTTP API through Graft without writing a source-based app first.

Even in proxy mode, the generated Graft server exposes both MCP and HTTP surfaces from a single server, with auto-served discovery and docs endpoints — the same thesis as source-based apps.

## Entry paths

- OpenAPI mode: `graft serve --openapi ./openapi.yaml --target <base-url>`
- Config mode: `graft serve --config ./graft.proxy.yaml`
- Check mode uses the same source inputs through `graft check --openapi ...` or `graft check --config ...`

## Curation guidance

- Do not expose every upstream endpoint to MCP by default.
- Keep the MCP-visible surface focused on agent-relevant operations.
- Rename operations and tighten descriptions when the generated names are vague.
- Make mutating operations explicit and protect them with auth when needed.

## Current proxy-facing realities

- The generated server exposes MCP over `POST /mcp`.
- The proxy server auto-serves the same framework endpoints as source-based apps: `/.well-known/agent.json`, `/.well-known/mcp.json`, `/openapi.json`, `/docs`, `/llms.txt`, `/llms-full.txt`, `/health`.
- If documenting `parameterLocations.name`, describe it only for `header` and `query` remapping, not `body` or `path`.
- `--header` defines caller-overridable defaults.
- `--locked-header` defines operator-controlled headers that callers cannot override.

## Documentation defaults

- Show one minimal OpenAPI command example and one minimal `graft.proxy.yaml` example.
- If the task is docs or review work, compare examples against the current CLI flags and transport tests instead of assuming older behavior.
- Mention the auto-served discovery and docs surface when documenting proxy deployments — agents discover proxy tools the same way they discover source-app tools.
- Reference the CLI commands available in proxy mode: `serve`, `dev`, `check`, `studio` (note: `test` and `add-tool` are source-app only).
