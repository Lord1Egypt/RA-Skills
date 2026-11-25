> Detailed usage and architecture reference. [Quick overview](../../../README.md).


# VMware VDI

[![PyPI](https://img.shields.io/pypi/v/vmware-vdi)](https://pypi.org/project/vmware-vdi/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#readme-license)

English | [中文](detailed-guide-CN.md)

Maintainer: Wei Zhou · [zhouwei008@gmail.com](mailto:zhouwei008@gmail.com)

Community-maintained open-source project; not an official VMware or Broadcom product.

[Overview](#readme-overview) · [Quick Start](#readme-quick-start) · [MCP Configuration](#readme-mcp-configuration) · [Capabilities and Workflows](#readme-capabilities-and-workflows) · [Safety and Audit](#readme-safety-and-audit) · [Troubleshooting](#readme-troubleshooting) · [Companion Skills](#readme-companion-skills) · [Reference](#readme-reference) · [License](#readme-license)

<a id="readme-overview"></a>

## Overview

Runs locally over stdio by default; configure required targets and credentials on your own machine.

**AI-powered intelligent operations for VMware / Omnissa Horizon VDI** — manage desktop pools, RDS farms,
published apps, **user sessions**, desktop machines, entitlements, instant-clone images, and Horizon
events/health/statistics through the **Horizon 8 Connection Server REST API**. Ships as both an **MCP
server** (for AI agents) and a **CLI** (for help-desk and scripting). Part of the
[VMware skill family](#companion-skills).

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or
> sponsored by VMware, Inc., Broadcom Inc., or Omnissa, LLC.** "VMware", "Horizon", and "Omnissa" are
> trademarks of their respective owners. Source is publicly auditable under the MIT license.

> **Status: v1.0.0 (beta).** REST endpoints are verified against the official Horizon Server API;
> GET-response field projections are defensive and pending validation against a live Connection Server
> (a field-name mismatch yields empty results, not a crash — see the [beta note](#beta-note)).

For field-projection problems, share only a minimal, redacted diagnostic example. Remove user identities, session IDs, machine/host names, internal addresses and credentials before opening an issue.

Full agent instructions: [`skills/vmware-vdi/SKILL.md`](../../../skills/vmware-vdi/SKILL.md).

<a id="readme-quick-start"></a>

## Quick Start

Requires Python `>=3.10` and `uv`.

```bash
uv tool install vmware-vdi==2.4.6
vmware-vdi --help
```

Target, credential and local data setup: [setup guide](../../../skills/vmware-vdi/references/setup-guide.md).

<details>
<summary>Installation and configuration details (including offline setup)</summary>

### Quick start

```bash
uv tool install vmware-vdi==2.4.6
vmware-vdi init      # friendly wizard: connect to a Connection Server + discover your pools
vmware-vdi doctor    # verify config / credentials / connectivity
vmware-vdi health    # one-glance VDI health
```

`vmware-vdi init` prompts for the Connection Server host, admin username, AD domain, and password; writes
`~/.vmware-vdi/config.yaml` + a `0600` `.env` (password obfuscated); tests the login; and on success
**discovers your pools, machines, and sessions** with the next commands to try.


</details>

<a id="readme-mcp-configuration"></a>

## MCP Configuration

Copy this configuration into your MCP client's local stdio settings. The client must be able to find `uvx`; the initial package installation requires access to a package index.

```json
{
  "mcpServers": {
    "vmware-vdi": {
      "command": "uvx",
      "args": ["--from", "vmware-vdi==2.4.6", "vmware-vdi-mcp"],
      "env": {
        "VMWARE_VDI_CONFIG": "~/.vmware-vdi/config.yaml"
      }
    }
  }
}
```

The following sections retain preinstalled CLI alternatives and product-specific MCP options.

<details>
<summary>Preinstalled CLI and additional MCP options</summary>

### MCP server

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


</details>

<a id="readme-capabilities-and-workflows"></a>

## Capabilities and Workflows

### Why vmware-vdi

Every other VMware family skill stops at the vСenter VM. **A Horizon desktop pool sits *on* those VMs** —
so `vmware-aiops` can reset the backing VM, but it cannot see a *user session*, log a user off, disable a
*pool*, or push a golden image. `vmware-vdi` fills exactly that day-2 VDI gap — "who is stuck on a broken
desktop", "log this user off so their profile unlocks", "why is this pool not provisioning", "push the
patched image to Finance tonight" — with the family's **governed-ops harness**: every write is audited,
previews its blast radius, and is authorized by the Horizon account's own RBAC role.

### Capabilities — 27 MCP tools (16 read / 11 write)

| Category | Tools |
|----------|-------|
| **Monitoring** | health summary · session list/get · machine list/get · event list |
| **Statistics** | session concurrency stats · per-pool utilization |
| **Management** | pool list/get · farm list · app-pool list · entitlement list · image list · AD search · pool enable/disable · entitlement add/remove |
| **Ops actions** | session logoff / disconnect / message · machine reset / maintenance / remove |
| **Tasks** | task status · **image push** · task cancel |

Entitlement reads accept Horizon's single `EntitlementInfo` object as well as paginated principal rows.
When Horizon returns only SIDs, principal names remain empty and types are `UNKNOWN`; an unreadable
response is an error, rather than evidence that nobody is entitled.

Reads are strictly non-destructive. Writes **preview their blast radius**, double-confirm at the CLI, and
are audit-logged to `~/.vmware/audit.db`. `push_desktop_pool_image` recreates *every desktop in a pool* — the
highest single-call blast radius in the family — and its preview states affected-desktop and
in-session counts before any confirm, together with `occupancy`: `determined` when those counts
can be believed, `unknown` when sessions exist that cannot be attributed to any pool or farm. An
`unknown` occupancy refuses the confirm rather than reporting an unverified zero; overriding it
needs `--acknowledge-unknown-occupancy` and is recorded in the audit row. A machine that names no
desktop pool also makes the desktop count a lower bound ("at least N"); that refuses the confirm
with no override.

On MCP, every gated write takes `confirm` (default `false`). A call without it returns `blast_radius` —
the object's identity, counts, identifiers up to 20, `blockers` and `unmeasured` — and changes nothing;
the acting response carries the same dict. An agent should show it to the user and pass `confirm=true`
only after they agree. When something the blast radius depends on could not be read — a machine's
state, a session's user, a task's type or state, a pool's enabled flag, a pool's current entitlements —
`confirm=true` is refused with a message naming what to check.

### Example workflows

**Help-desk — a user's desktop is stuck**
```bash
vmware-vdi session list --user alice
vmware-vdi machine list --state AGENT_UNREACHABLE
vmware-vdi session logoff --user alice --dry-run   # preview which sessions
vmware-vdi session logoff --user alice             # double-confirm, then logs off + audits
```

**Patch night — push a new golden image**
```bash
vmware-vdi image list
vmware-vdi pool push-image --id pool-fin --dry-run  # BLAST RADIUS: N desktops, M logged-in users
vmware-vdi pool push-image --id pool-fin            # double-confirm; returns a task
vmware-vdi task status --pool pool-fin              # track progress
```

<a id="readme-safety-and-audit"></a>

## Safety and Audit

### Security

- **Authorization = Horizon RBAC.** The skill does not gate read vs write; point a target at a **read-only
  Horizon admin role** and every write is refused at the Connection Server, un-bypassably.
- **Credentials** live only in `~/.vmware-vdi/.env` (`0600`, obfuscated `b64:` at rest); config files hold
  host/username/domain only. Inject `VMWARE_VDI_<TARGET>_PASSWORD` from a secret manager for real secrecy.
- **TLS** verification on by default. All Connection-Server text is `sanitize()`d against prompt injection.
- **No outbound calls** except to the configured Connection Server — no webhooks, no telemetry.

See [`SECURITY.md`](../../../SECURITY.md) and `skills/vmware-vdi/references/setup-guide.md`.

### Remote access (HTTPS) and limiting tools

By default `vmware-vdi mcp` speaks stdio to one local client and offers every tool. Two options change that
(vmware-policy ≥ 1.21.0).

**Serve over HTTPS** so clients on other machines can connect. Every caller needs a bearer token:

```bash
vmware-audit token create alice          # prints the token once; give it to alice
vmware-audit token list                  # names only
vmware-audit token revoke alice          # refused from its next request, no restart
vmware-vdi mcp --transport https --host 0.0.0.0 --port 8443 \
    --cert /etc/vmware-mcp/server.pem --key /etc/vmware-mcp/server-key.pem \
    --public-name mcp.example.com
```

Connect a client (Claude Code shown; any MCP client that supports streamable HTTP and custom headers works):

```bash
claude mcp add --transport http vmware-vdi https://mcp.example.com:8443/mcp \
    --header "Authorization: Bearer $VMWARE_MCP_TOKEN"
```

```json
{
  "mcpServers": {
    "vmware-vdi": {
      "type": "http",
      "url": "https://mcp.example.com:8443/mcp",
      "headers": { "Authorization": "Bearer ${VMWARE_MCP_TOKEN}" }
    }
  }
}
```

- The server will not start without a token, refuses Host/Origin values outside `--public-name`, and checks
  before it binds that unauthenticated requests get 401. Use a certificate your clients trust for those names.
- Behind a TLS-terminating reverse proxy on the same machine use `--transport http --host 127.0.0.1
  --public-name mcp.example.com` and pass the `Authorization` header through.
- Behind a load balancer or gateway on another machine, keep `--transport https` (a self-signed certificate is
  fine), list in `--public-name` the host name the balancer sends as `Host`, and have it forward `Authorization`.
  Its health probe can use `GET /healthz`, which needs no token and returns only `{"status": "ok"}`
  (vmware-policy ≥ 1.23.0).
- Send `traceparent` or `X-Request-ID` with each request to have it stored on the audit row;
  `vmware-audit log --correlation-id ID` then finds the calls behind one platform request.
- The audit log records each caller as `token:<name>`. Calls run side by side, with or without a target: each
  target keeps up to `VMWARE_MCP_POOL_SIZE` sessions (default 2), and each session is a login on the target. A call
  that finds them all busy waits at most 300 s for one.
- **Everyone who can reach the endpoint acts with this server's account.** Tokens identify callers; they grant
  nothing on the platform. Run one endpoint per privilege level.
- **Several people or roles on one endpoint:** run `vmware-audit roles enable` once, then give each token a role (`vmware-audit token create NAME --role reader`, or a role in `roles.yaml` naming tools and targets; vmware-policy ≥ 1.24.0). A role limits what the token may call on this endpoint; it cannot grant more than the account has. See vmware-policy's README, "Roles for network callers".

**Offer only read tools, plus the writes you choose:**

```bash
vmware-vdi mcp --expose read --allow-write add_entitlement
# or: VMWARE_VDI_MCP_EXPOSE=read VMWARE_VDI_MCP_ALLOW_WRITE=add_entitlement vmware-vdi mcp
```

Tools not offered do not appear in the client's tool list. A bad value or an unknown write tool stops the server
(exit 2). This limits what clients are offered; it is not authorization, so the account itself should be
least-privilege.

Details: `skills/vmware-vdi/references/setup-guide.md` ("Serving MCP over HTTPS", "Limiting which tools are offered").

<a id="readme-troubleshooting"></a>

## Troubleshooting

### System proxy bypass

The Horizon REST client honors the operating system proxy bypass list for the configured origin.
TLS verification still follows `verify_ssl`, and CA environment settings such as `SSL_CERT_FILE` remain active.
Other origins retain their normal proxy routing.

<a id="readme-companion-skills"></a>

## Companion Skills

The VMware Skills family contains 14 MCP servers and the shared Policy library. Choose tools by responsibility: [vmware-skills](https://github.com/vmware-skills).

### Companion skills

Part of the VMware skill family — install the modules you need:

- **[vmware-aiops](https://github.com/vmware-skills/VMware-AIops)** — the vCenter VMs backing the desktops (power, snapshot, clone, migrate)
- **[vmware-monitor](https://github.com/vmware-skills/VMware-Monitor)** — read-only vSphere monitoring
- **[vmware-nsx-security](https://github.com/vmware-skills/VMware-NSX-Security)** — desktop network microsegmentation
- **[vmware-aria](https://github.com/vmware-skills/VMware-Aria)** · **[vmware-nsx](https://github.com/vmware-skills/VMware-NSX)** · **[vmware-storage](https://github.com/vmware-skills/VMware-Storage)** · **[vmware-vks](https://github.com/vmware-skills/VMware-VKS)** · **[vmware-avi](https://github.com/vmware-skills/VMware-AVI)** · **[vmware-harden](https://github.com/vmware-skills/VMware-Harden)**

<!-- usage: remote-and-exposure -->

<a id="readme-reference"></a>

## Reference

Release history: [RELEASE_NOTES.md](../../../RELEASE_NOTES.md).

Read-only self-test with your own model and agent host: [model-fit self-test](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

### Upgrading to 2.0

2.0 renames all 27 MCP tools so every name starts with a verb (e.g. `ad_user_search` → `search_ad_users`, `app_pool_list` → `list_app_pools`, `entitlement_add` → `add_entitlement`). The full old → new table is in
[RELEASE_NOTES.md](../../../RELEASE_NOTES.md#v200--mcp-tools-renamed-verb-first). Nothing else changes: same tools, parameters,
safety gates and CLI commands. If an agent prompt, script or `~/.vmware/rules.yaml` names a tool, update it — though deny
rules written with the old names keep working with vmware-policy ≥ 1.18 (`vmware-audit policy` lists any rule the
renames widened), and vmware-pilot ≥ 1.13 translates old names in saved workflows.
If an install older than 2.0 shares that `rules.yaml`, give it vmware-policy ≥ 1.18.2 too: it matches each rule
against both the old and the new name, so one file serves both.

### Supported versions

- **VMware Horizon 8.x** (primary) — Connection Server REST API `/rest/v1`.
- **Latest Omnissa Horizon** (2406 / 2412+) — same `/rest/v1` lineage.

### Beta note

REST **endpoints** are verified against the official Horizon Server API operation index. GET-response
**field names** (and a few write bodies) are defensive (`.get()` with fallbacks) and **pending validation
against a live Connection Server**. On a field-name mismatch a list reads empty rather than crashing.
First real-Horizon use should run `vmware-vdi init` and confirm the session/machine/pool projections;
please [file an issue](https://github.com/vmware-skills/VMware-VDI/issues) with a minimal, redacted `*_get` example if a projection
looks empty. Remove user identities, session IDs, machine/host names, internal addresses and credentials before sharing. Quality: 32 regression tests, ruff clean, bandit 0, tool endpoints pinned to a verified spec.

<a id="readme-license"></a>

Unrecognized collection responses and exhausted pagination budgets fail before write previews or confirmed changes use an incomplete inventory. Neither confirm nor acknowledgement of unknown occupancy bypasses this refusal. Horizon positive appliance validation is still pending.

## License

MIT — see [LICENSE](../../../LICENSE).

### Transient request recovery

Only GET requests are automatically retried after a transport failure or a
502/503/504 response. Writes are sent once even when a retry budget is supplied:
a missing response may mean the change already took effect. Inspect the target
before retrying a write. A single authentication recovery after an explicit
rejection is handled separately. This boundary has synthetic HTTP contract
coverage; it does not establish positive appliance compatibility.
