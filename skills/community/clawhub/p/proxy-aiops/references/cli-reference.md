# proxy-aiops — CLI reference

Global option on most commands: `--target/-t <name>` (default: first target in
config).

## Setup & health

```bash
proxy-aiops init                 # interactive wizard: platform, base_url, TLS verify, encrypted secret
proxy-aiops doctor               # config + secrets + connectivity (probe per platform)
proxy-aiops doctor --skip-auth   # skip the connectivity probe
proxy-aiops overview             # one-shot: version + routes/services + upstream health
```

## Reads

```bash
proxy-aiops routes list [--host app.example.com]
proxy-aiops routes show <name>              # traefik router name / caddy config path / haproxy frontend
proxy-aiops routes find <host> [--path /]   # which routes would serve host/path
proxy-aiops services list
proxy-aiops services show <name>
proxy-aiops services upstreams [--service <name>]
proxy-aiops certs [--sweep] [--warn-days 30] [--critical-days 7] [--port 443]
proxy-aiops config snapshot
proxy-aiops config search <query>
proxy-aiops config get <path>
```

## Flagship analyses

```bash
proxy-aiops analyze health [--service <name>]   # backend/upstream health RCA
proxy-aiops analyze errors [--rate 5.0] [--min-requests 30]   # 5xx error-rate RCA
proxy-aiops analyze conflicts                   # shadowed/dead routes, redirect loops
```

## Governed writes (dry-run + double-confirm; audited + undo-recorded)

```bash
# caddy config (teaching error on traefik/haproxy targets)
proxy-aiops config set <path> '<json>' [--dry-run]
proxy-aiops config delete <path> [--dry-run]        # risk=high, double-confirm

# haproxy runtime servers (teaching error on traefik/caddy targets)
proxy-aiops server state <backend> <server> ready|drain|maint [--dry-run]
proxy-aiops server weight <backend> <server> <0-256> [--dry-run]
```

High-risk writes prompt for double confirmation at the CLI. Optionally export
`PROXY_AUDIT_APPROVED_BY` (and `PROXY_AUDIT_RATIONALE`) to annotate the audit
row with who/why — never required.

## Secrets

```bash
proxy-aiops secret set <target>      # store encrypted (hidden prompt)
proxy-aiops secret list              # names only, never values
proxy-aiops secret rm <target>
proxy-aiops secret migrate           # import legacy plaintext .env
proxy-aiops secret rotate-password   # re-encrypt under a new master password
```

## MCP server

```bash
proxy-aiops mcp        # stdio transport (or: proxy-aiops-mcp)
```

## Environment variables

| Variable | Purpose |
|----------|---------|
| `PROXY_AIOPS_MASTER_PASSWORD` | unlock secrets.enc non-interactively (MCP/CI) |
| `PROXY_AIOPS_CONFIG` | alternate config.yaml path (MCP server) |
| `PROXY_AIOPS_HOME` | relocate config/audit/undo state dir |
| `PROXY_AUDIT_APPROVED_BY` / `PROXY_AUDIT_RATIONALE` | optional approver/rationale annotations recorded on the audit row |
| `PROXY_MAX_TOOL_CALLS` / `PROXY_MAX_TOOL_SECONDS` | per-process budget ceilings |
| `PROXY_RUNAWAY_MAX` / `PROXY_RUNAWAY_WINDOW_SEC` | runaway circuit-breaker tuning |
| `PROXY_<TARGET>_SECRET` | legacy plaintext fallback (deprecated) |
