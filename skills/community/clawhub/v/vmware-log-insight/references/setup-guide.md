# vmware-log-insight Setup Guide

## Install

```bash
uv tool install vmware-log-insight==2.4.4
mkdir -p ~/.vmware-log-insight
cp config.example.yaml ~/.vmware-log-insight/config.yaml
```

## Configure targets

Edit `~/.vmware-log-insight/config.yaml`:

```yaml
targets:
  prod:
    host: loginsight.example.com
    username: admin
    port: 9543            # public API port (default 9543)
    verify_ssl: true
    provider: Local       # Local | ActiveDirectory | <vIDM provider name>
    environment: production   # production | staging | lab — see below
default_target: prod
```

### `environment` — an optional label

`environment` is an optional free-form label on a target. An environment-scoped
`deny` rule in `~/.vmware/rules.yaml` can match on it — for example, to freeze
writes on `production`; a target with no label is simply not matched by such a
rule.

Every tool this skill ships is read-only, and reads are never gated — so the
label changes nothing for Log Insight today. Set it anyway to keep the family's
config files consistent, so a future write tool is correctly scoped. Run
`vmware-audit policy` to see the rules in force.

## Credentials

Passwords are **never** stored in `config.yaml`. Set the per-target env var:

```bash
# ~/.vmware-log-insight/.env  (chmod 600)
VMWARE_LOG_INSIGHT_PROD_PASSWORD=yourpassword
```

```bash
chmod 600 ~/.vmware-log-insight/.env
```

The env var name is `VMWARE_LOG_INSIGHT_<TARGET>_PASSWORD` where `<TARGET>` is the
upper-cased target name (hyphens → underscores).

### Password obfuscation at rest

On first load, any plaintext `*_PASSWORD` value in `.env` is automatically
rewritten to a grep-safe `b64:<encoded>` form and decoded transparently at
runtime, so a casual `grep` of the file no longer reveals the password. Values
are read/written through python-dotenv's own parser, so the stored secret never
drifts from what you configured.

> **This is obfuscation, not encryption.** Anyone who can read the file can still
> decode it. For real secrecy at rest, do not store the password in `.env` at all —
> inject it from a secret manager (HashiCorp Vault, CyberArk, AWS Secrets Manager,
> or a Kubernetes Secret) into the `VMWARE_LOG_INSIGHT_<TARGET>_PASSWORD`
> environment variable at process start. The code reads the env var either way:
> ```bash
> export VMWARE_LOG_INSIGHT_PROD_PASSWORD="$(vault kv get -field=password secret/loginsight/prod)"
> vmware-log-insight mcp
> ```

## Verify

```bash
vmware-log-insight doctor
```

Checks: config file, `.env` permissions, config parse, password env vars, network
reachability (TCP 9543), authentication, appliance version, MCP server import.

## MCP client configuration

```json
{
  "command": "uvx",
  "args": ["--from", "vmware-log-insight==2.4.4", "vmware-log-insight-mcp"],
  "env": { "VMWARE_LOG_INSIGHT_CONFIG": "~/.vmware-log-insight/config.yaml" }
}
```

If you installed with `uv tool install`, prefer the entry point `vmware-log-insight mcp`
(no PyPI resolution at startup — robust behind corporate TLS proxies, 踩坑 #25).

## Serving MCP over HTTPS

By default the MCP server speaks stdio to one local client. To let clients on other machines reach it, serve it over
HTTPS. Every caller then needs a bearer token.

```bash
vmware-audit token create alice                      # prints the token once; give it to alice
vmware-log-insight mcp --transport https --host 0.0.0.0 --port 8443 \
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

## Behind an MCP gateway

A gateway (one MCP endpoint in front of several servers, for example vmware-monitor, vmware-aria and
vmware-log-insight) works with these servers as they are: each backend runs as in
[Serving MCP over HTTPS](#serving-mcp-over-https), and the gateway is just another client. Tool names do not
collide across vmware-monitor, vmware-aria and vmware-log-insight, so the gateway needs no prefixes. What to
decide:

- **Who the backend sees.** If the gateway calls every backend with one token of its own, every audit row says
  `token:<gateway>` and per-caller roles stop meaning anything. To keep per-person audit and roles, have the gateway
  **forward each caller's own `Authorization` header** to the backend. Servers on one host with the same `OPS_HOME`
  (default `~/.vmware`) share one token file, so one token per person works on all of them. A backend session is
  bound to the token that opened it, so the gateway must open a backend session per caller, not share one. If the gateway does
  its own authentication instead, give it a token per backend and accept that audit identifies the gateway, not
  the person; forward `traceparent` or `X-Request-ID` so `vmware-audit log --correlation-id ID` still ties calls to
  one platform request.
- **Read-only does not depend on the gateway.** Keep the layers on each backend: a read-only platform account (the
  real boundary), `--expose read` so write tools are never offered, and deny rules in `~/.vmware/rules.yaml`. A
  gateway misconfiguration then cannot turn into a write.
- **Tool list size is the main cost, not the extra hop.** The hop adds milliseconds; platform calls take hundreds
  of milliseconds to seconds. But clients put every offered tool's schema into the model's context on every turn.
  Even with `--expose read`, the schemas of vmware-monitor, vmware-aria and vmware-log-insight together come to
  about 30,000 tokens or more. Offer the gateway's clients a curated subset, or group
  tools per task, rather than passing all of them through.
- **Timeouts and sessions.** Set the gateway's per-call timeout above the longest call you expect: a call can wait
  up to 300 s for a free session to a busy target. A backend MCP session expires after 30 minutes idle; the gateway
  must start a new session when the backend answers 404 for an old one, as the MCP specification requires.
- **Scaling.** Run one backend endpoint per privilege level, not one per caller. Add sessions per target with
  `VMWARE_MCP_POOL_SIZE` before adding processes. Point the gateway's health checks at `GET /healthz`.

## Security

> **Disclaimer**: Community-maintained open-source project, **not affiliated with,
> endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.**

1. **Source Code** — https://github.com/vmware-skills/VMware-Log-Insight (MIT).
2. **Config file contents** — `config.yaml` holds only host/port/username/provider;
   no passwords or tokens. Secrets live only in `.env` (`chmod 600`).
3. **Webhook data scope** — none. This skill makes no outbound calls except to the
   configured Log Insight appliance.
4. **TLS verification** — on by default (`verify_ssl: true`); disable only for
   self-signed lab appliances.
5. **Prompt-injection protection** — all API text passes through `sanitize()`
   (truncation + C0/C1 control-char stripping).
6. **Least privilege** — use a read-only Log Insight service account; this skill
   only reads (events, aggregations, fields, alerts) and never writes.

**The account is the boundary.** This skill has no write tools, but an agent that can run shell commands can reach
the platform without it (SSH, curl, govc, PowerCLI). Give the service account only the read privileges it needs;
nothing in the skill can stop the same credentials being used another way.

