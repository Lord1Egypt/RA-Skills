# vmware-debug Setup Guide

vmware-debug needs **no VMware endpoint configuration or VMware credentials** — it
is a pure, offline correlation engine. There is no `config.yaml` and no `.env`.

Default stdio has no listener. Opt-in HTTPS uses caller bearer tokens and TLS
certificate/key files and opens the configured listener. Case tools write a local
ledger; every tool also writes the separate `~/.vmware/audit.db` audit trail.

## Install

```bash
uv tool install vmware-debug==2.3.3
vmware-debug categories      # verify it runs
```

## MCP client configuration

```json
{
  "command": "uvx",
  "args": ["--from", "vmware-debug==2.3.3", "vmware-debug-mcp"]
}
```

If installed with `uv tool install`, prefer the entry point `vmware-debug mcp`
(no PyPI resolution at startup — robust behind corporate TLS proxies, 踩坑 #25).

For full cross-skill diagnosis, also install the data-source skills it correlates
(vmware-monitor, vmware-log-insight, vmware-aria, vmware-nsx) and the executors it
routes fixes to (vmware-aiops, vmware-pilot).

## Limiting which tools are offered

By default the MCP server offers every tool. To offer only read tools, start it with `--expose read`, or set
`VMWARE_DEBUG_MCP_EXPOSE=read` in the MCP client's `env` block (useful when the client launches `vmware-debug mcp` itself). To offer
chosen write tools as well, add `--allow-write` with a comma-separated list (or `VMWARE_DEBUG_MCP_ALLOW_WRITE`):

```bash
vmware-debug mcp --expose read --allow-write close_case
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
  `vmware_policy.exposure.restrict_tools(mcp, skill="debug", expose="read", allow_write=[...])` before running it,
  instead of editing the SDK's tool registry.
- This limits what clients are offered. It is **not** authorization. This server's write tools change case records on this machine;
  deny rules in `~/.vmware/rules.yaml` still apply to every exposed tool.

## Serving MCP over HTTPS

By default the MCP server speaks stdio to one local client. To let clients on other machines reach it, serve it over
HTTPS. Every caller then needs a bearer token.

```bash
vmware-audit token create alice                      # prints the token once; give it to alice
vmware-debug mcp --transport https --host 0.0.0.0 --port 8443 \
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
- Each audit row records the caller as `token:<name>`. Calls naming different targets run in parallel; calls that
  name no target run one at a time, so name the target when several people use one server.
- **Everyone who can reach the endpoint acts with this server's account.** Tokens identify callers; they grant
  nothing on the platform. Run one endpoint per privilege level (for example a read-only account behind
  `--expose read`, and a separate endpoint for operators).
- **Several people or roles on one endpoint:** run `vmware-audit roles enable` once, then give each token a role (`vmware-audit token create NAME --role reader`, or a role in `roles.yaml` naming tools and targets; vmware-policy ≥ 1.24.0). A role limits what the token may call on this endpoint; it cannot grant more than the account has. See vmware-policy's README, "Roles for network callers".

## Security

> **Disclaimer**: Community-maintained open-source project, **not affiliated with,
> endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.**

1. **Source Code** — https://github.com/vmware-skills/VMware-Debug (MIT).
2. **Credentials** — no VMware account credentials. Optional HTTPS uses caller
   bearer tokens and TLS certificate/key files; protect them as secrets.
3. **Network** — the correlation tools make no VMware API calls. Default stdio has
   no listener; optional HTTPS opens the configured listener. The case tools write local files.
4. **Writes** — case operations update the local investigation ledger under `$OPS_HOME`; every tool also writes the separate audit database
   (the seven [WRITE] case tools). Evidence, gaps, hypotheses and grade
   history are only ever added to; `timeline.md` is regenerated from the evidence and
   `case.json` holds the current grade and state. Nothing is written to any
   VMware system: debug only diagnoses and recommends; remediation is routed
   to vmware-aiops / vmware-pilot, where confirmation/approval/audit live.
   Case data is sensitive: each case folder (`$OPS_HOME/cases/<case-id>/`, default
   `~/.vmware/cases/`) is created owner-only (`0700`) and holds the submitted
   evidence — host names, addresses, log and event text. There is no automatic
   retention limit: `close_case` marks a case closed and keeps its files; delete
   the folder to remove a case.
5. **No cross-skill coupling** — events arrive as plain dicts (the event
   envelope); debug imports no other skill package at runtime.
6. **Environment scoping** — policy rules can scope by environment, and skills
   that connect to a VMware estate may declare `environment:` (`production` /
   `staging` / `lab`) per target in their own `config.yaml` as an optional label
   an environment-scoped `deny` rule can match on. debug has no config and no
   connection to declare one about, so it registers no environment resolver —
   it has no basis to answer for any target — and an environment-scoped rule
   never matches its tools. Every other policy rule does apply: each MCP tool
   and the `categories` / `triage` CLI commands pass through vmware-policy's
   `guard()`. Verified behaviour:
   - A `deny` rule naming a debug tool, or with no `operations` key at all,
     refuses it (status `denied`, with the rule's reason).
   - A malformed `~/.vmware/rules.yaml` fails closed: every tool is refused with
     a reason naming the file and the way out (fix it, or
     `VMWARE_POLICY_DISABLED=1`). The `categories` and `triage` commands exit 1
     with a Python traceback whose last lines are that message; `version` and
     `mcp` are unaffected.
   - Runaway guard: within one MCP server process, the 26th call to the same
     tool with identical arguments inside 120 s is refused (`budget_exceeded`).
     Tune with `VMWARE_RUNAWAY_MAX` / `VMWARE_RUNAWAY_WINDOW_SEC`. The guard
     compares a SHA-256 digest of the arguments the tool actually received
     (vmware-policy ≥1.16.0), not the redacted copy in the audit row — so calls
     with different `events` or `payload` are never counted as identical.
   - A `maintenance_window` gates only `high`/`critical` risk operations; every
     debug tool is `low`, so a window never blocks one.
7. **Audit row contents** — one row per call in `~/.vmware/audit.db`: tool,
   time, OS user, detected agent, arguments, status and result. `payload` and
   `events` are stored as `***`. The results of `build_incident_timeline` and
   `record_case_timeline` are not stored (`[redacted: return value declared
   sensitive]`) because they quote event text; other results are stored after
   credential scrubbing. The status is still truthful — a call that returns
   `{"error": …}` is `error`.
8. **Static analysis** — `uvx bandit==1.9.4 -r vmware_debug/` (release bar:
   0 Medium+).
