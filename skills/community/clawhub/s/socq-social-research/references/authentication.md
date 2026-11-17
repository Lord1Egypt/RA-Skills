# Authentication

Set `SOCQ_API_KEY` in the process environment. The hosted MCP server and CLI accept the same `sk-...` key used by the Agent REST API.

Credential priority for the CLI:

1. `--api-key` for one-off automation only.
2. `SOCQ_API_KEY`.
3. The local config written by `socq auth login`.

Avoid `--api-key` during interactive use because shells commonly retain command history. Do not put keys in MCP URLs. The stdio bridge reads the key locally and forwards it as `Authorization: Bearer ...`.

Useful setup commands:

```bash
socq auth login
socq auth status
socq auth clear
```

An API key can enforce an IP allowlist, per-minute request rate, and hourly or daily credit limits. A 403 may therefore be an IP policy failure even when the key is valid.
