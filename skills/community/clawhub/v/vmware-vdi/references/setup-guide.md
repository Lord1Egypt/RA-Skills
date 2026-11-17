# vmware-vdi — Setup Guide

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or
> sponsored by VMware, Inc., Broadcom Inc., or Omnissa, LLC.**

## 1. Install
```bash
uv tool install vmware-vdi==2.4.5
```

## 2. Connect (friendly wizard)
```bash
vmware-vdi init
```
Prompts for the **Connection Server host**, admin **username**, AD **domain** (blank for a local admin),
**password**, target name, and TLS verification. It writes `~/.vmware-vdi/config.yaml` +
`~/.vmware-vdi/.env` (chmod 600), tests `/rest/login`, and on success **discovers your pools/machines/
sessions** and prints the next commands to try. Re-run with `--force` to add another Connection Server
(existing targets are preserved; the default is repointed to the new one).

Manual config (`~/.vmware-vdi/config.yaml`):
```yaml
default_target: prod
targets:
  prod:
    host: horizon-cs1.example.com
    username: svc-vdi-ro          # a read-only Horizon role for read commands
    domain: ACME                  # AD domain; blank for a local Connection Server admin
    port: 443
    verify_ssl: true              # false only for a self-signed lab cert
```
Password (never in config.yaml): `~/.vmware-vdi/.env`
```
VMWARE_VDI_PROD_PASSWORD=b64:...    # written by `init`; or export it yourself (plaintext auto-obfuscated)
```

## 3. Verify
```bash
vmware-vdi doctor        # config / credentials / connectivity
```

## 4. Supported versions
- **Primary: VMware Horizon 8.x** (Connection Server REST API `/rest/v1`).
- **Latest Omnissa Horizon** (2406/2412+) — same `/rest/v1` lineage.
- Requires the Connection Server REST API enabled (Horizon 8.0+; audit-events since 2106).

## 5. MCP server
```json
{
  "mcpServers": {
    "vmware-vdi": {
      "command": "vmware-vdi",
      "args": ["mcp"],
      "env": { "VMWARE_VDI_CONFIG": "~/.vmware-vdi/config.yaml" }
    }
  }
}
```
Using the installed `vmware-vdi mcp` console script (not `uvx`) avoids a PyPI re-resolve on every launch —
important behind enterprise TLS proxies.

## Limiting which tools are offered

By default the MCP server offers every tool. To offer only read tools, start it with `--expose read`, or set
`VMWARE_VDI_MCP_EXPOSE=read` in the MCP client's `env` block (useful when the client launches `vmware-vdi mcp` itself). To offer
chosen write tools as well, add `--allow-write` with a comma-separated list (or `VMWARE_VDI_MCP_ALLOW_WRITE`):

```bash
vmware-vdi mcp --expose read --allow-write add_entitlement
```

- A read tool is one annotated `readOnlyHint: true`; every other tool counts as a write.
- An unknown setting, or a name that is not a write tool of this server, stops the server before it serves (exit
  code 2), so it never offers more than you asked for. Pre-2.0 tool names are accepted.
- With `--expose read`, the server prints one line to stderr saying what it exposes.
- Flags and environment variables are not mixed: if either flag is given, both environment variables are
  ignored, so a leftover `_ALLOW_WRITE` in the shell cannot widen `--expose read`. A blank flag value counts as
  not given.
- A tool that runs other steps (a plan, workflow or batch tool) carries every write it can execute, including
  writes this setting hides. Expose such a tool only if you would expose those writes too.
- A launcher that imports the server object can call
  `vmware_policy.exposure.restrict_tools(mcp, skill="vdi", expose="read", allow_write=[...])` before running it,
  instead of editing the SDK's tool registry.
- This limits what clients are offered. It is **not** authorization: whether a call may change anything is decided by
  the account's permissions, and deny rules in `~/.vmware/rules.yaml` still apply to every exposed tool.
- An agent that can run shell commands can also reach the platform without MCP (SSH, curl, govc, PowerCLI). So
  the service account itself must be least-privilege: exposure and deny rules are guardrails, not the boundary.

## Serving MCP over HTTPS

By default the MCP server speaks stdio to one local client. To let clients on other machines reach it, serve it over
HTTPS. Every caller then needs a bearer token.

```bash
vmware-audit token create alice                      # prints the token once; give it to alice
vmware-vdi mcp --transport https --host 0.0.0.0 --port 8443 \
    --cert /etc/vmware-mcp/server.pem --key /etc/vmware-mcp/server-key.pem \
    --public-name mcp.example.com
```

- Clients connect to `https://mcp.example.com:8443/mcp` and send `Authorization: Bearer <token>`.
- `--public-name` lists every host name clients use (comma-separated); requests for any other Host or Origin are
  refused. Use a certificate your clients trust for those names.
- Behind a reverse proxy that terminates TLS (Nginx, HAProxy) on the same machine, use
  `--transport http --host 127.0.0.1 --public-name mcp.example.com` (the names the proxy forwards in `Host`), and
  have the proxy pass the `Authorization` header through.
- Behind a load balancer or gateway on another machine, keep `--transport https` (a self-signed certificate is
  fine: the balancer is the client that has to trust it), list in `--public-name` the host name the balancer sends
  as `Host`, and have it forward `Authorization`. Point its health probe at `GET /healthz`: it needs no token, returns
  only `{"status": "ok"}` and accepts any `Host` (vmware-policy ≥ 1.23.0). Every other path still needs the token.
- Correlation: each audit row stores the caller's `traceparent` trace-id, else its `X-Request-ID` /
  `X-Correlation-ID`. Have the agent platform send one, and `vmware-audit log --correlation-id ID` lists the calls
  behind one platform request.
- `vmware-audit token list` / `token revoke NAME` manage callers; a revoked token is refused from its next request.
  Replace a leaked token under a new name.
- The server will not start without at least one token, and checks before it binds that unauthenticated requests
  are refused.
- Each audit row records the caller as `token:<name>`. Calls run side by side, with or without a target: each
  target keeps up to `VMWARE_MCP_POOL_SIZE` sessions (default 2), and each session is a login on the target. A call
  that finds them all busy waits at most 300 s for one.
- **Everyone who can reach the endpoint acts with this server's account.** Tokens identify callers; they grant
  nothing on the platform. Run one endpoint per privilege level (for example a read-only account behind
  `--expose read`, and a separate endpoint for operators).
- **Several people or roles on one endpoint:** run `vmware-audit roles enable` once, then give each token a role (`vmware-audit token create NAME --role reader`, or a role in `roles.yaml` naming tools and targets; vmware-policy ≥ 1.24.0). A role limits what the token may call on this endpoint; it cannot grant more than the account has. See vmware-policy's README, "Roles for network callers".

## Security
> **Disclaimer**: not affiliated with VMware/Broadcom/Omnissa.

- **Credentials**: password only in `~/.vmware-vdi/.env` (chmod 600, obfuscated `b64:` at rest —
  obfuscation, not encryption). For real secrecy, inject `VMWARE_VDI_<TARGET>_PASSWORD` from a secret
  manager (Vault / CyberArk / AWS SM / K8s Secret).
- **Authorization = RBAC**: the skill does not gate read vs write itself. Point a target at a **read-only
  Horizon admin role** and every write is refused at the Connection Server, un-bypassably.
- **TLS**: verification on by default; `verify_ssl: false` is per-target, for self-signed labs only.
- **Prompt-injection**: Connection-Server text is `sanitize()`d (truncated + control chars stripped).
- **Audit**: all writes recorded in `~/.vmware/audit.db` (SQLite WAL) via the shared `@vmware_tool` guard.
- **No outbound calls** other than to the configured Connection Server; no webhooks, no telemetry.
