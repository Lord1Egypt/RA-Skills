# vmware-debug Setup Guide

vmware-debug has **no configuration, no credentials, and no network access** — it
is a pure, offline correlation engine. There is no `config.yaml` and no `.env`.

## Install

```bash
uv tool install vmware-debug
vmware-debug categories      # verify it runs
```

## MCP client configuration

```json
{
  "command": "uvx",
  "args": ["--from", "vmware-debug", "vmware-debug-mcp"]
}
```

If installed with `uv tool install`, prefer the entry point `vmware-debug mcp`
(no PyPI resolution at startup — robust behind corporate TLS proxies, 踩坑 #25).

For full cross-skill diagnosis, also install the data-source skills it correlates
(vmware-monitor, vmware-log-insight, vmware-aria, vmware-nsx) and the executors it
routes fixes to (vmware-aiops, vmware-pilot).

## Security

> **Disclaimer**: Community-maintained open-source project, **not affiliated with,
> endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.**

1. **Source Code** — https://github.com/zw008/VMware-Debug (MIT).
2. **Credentials** — none. debug holds no secrets and connects to nothing.
3. **Network** — none. All tools are local pure functions over event data the
   agent supplies.
4. **Writes** — none. debug only diagnoses and recommends; remediation is routed
   to vmware-aiops / vmware-pilot, where confirmation/approval/audit live.
5. **No cross-skill coupling** — events arrive as plain dicts (the event
   envelope); debug imports no other skill package at runtime.
6. **Static analysis** — `uvx bandit -r vmware_debug/ mcp_server/` (release bar:
   0 Medium+).
