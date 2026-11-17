# xcpng-aiops — Setup & security guide

## Prerequisites

- A **Xen Orchestra instance** (XO from sources or the Xen Orchestra
  Appliance, 5.x) with the REST API at `/rest/v0`. XO is the management plane
  this tool talks to; your XCP-ng hosts/pools must already be connected to it
  (XO UI → Settings → Servers). **Per-host XAPI access is out of scope.**
- Python ≥ 3.11 (`uv tool install xcpng-aiops` handles the rest).

## 1. Create an XO authentication token

In the XO UI: user menu (top-right) → **Personal tokens** → create. Or from a
shell: `xo-cli --createToken`. Use a dedicated XO user with the least
privilege you can (admin is required for some collections; a read-mostly user
works for triage-only setups).

## 2. Onboard

```bash
xcpng-aiops init
```

The wizard prompts for:

1. **Master password** — encrypts `~/.xcpng-aiops/secrets.enc`. Never stored;
   export `XCPNG_AIOPS_MASTER_PASSWORD` for non-interactive use.
2. **Target name** (e.g. `xo1`) and the **XO URL** (e.g.
   `https://xo.example.com` — the same origin as the XO web UI).
3. **TLS verification** — default **yes**; answer no only for self-signed lab
   certificates.
4. **The token** (hidden input) — stored encrypted, never in config.yaml.

## 3. Verify

```bash
xcpng-aiops doctor
```

Checks: config present, encrypted store present + permissions (600), token
present per target, XO reachable, token valid (a 401/403 fails the check), and
how many XCP-ng pools the XO instance manages.

## Files & permissions

| Path | Content | Mode |
|------|---------|:----:|
| `~/.xcpng-aiops/config.yaml` | non-secret connection details | 700 dir |
| `~/.xcpng-aiops/secrets.enc` | Fernet-encrypted token map | 600 |
| `~/.xcpng-aiops/audit.db` | SQLite audit log (every tool call) | — |
| `~/.xcpng-aiops/undo.db` | recorded inverse descriptors | — |

Relocate everything with `XCPNG_AIOPS_HOME`.

## Security notes

- The token is sent per request as `Authorization: Bearer <token>` **and**
  `Cookie: authenticationToken=<token>` (compatibility across XO 5.x
  releases); held in memory only, never logged.
- Secret encryption: Fernet (AES-128-CBC + HMAC-SHA256), key derived from the
  master password via scrypt (N=2^15, r=8, p=1) with a random per-store salt.
- High-risk writes (`snapshot_delete`, `snapshot_revert`) require a `dry_run`
  preview + double confirmation at the CLI, and carry a `high` risk tier as a
  descriptive audit label — it gates nothing. `XCPNG_AUDIT_APPROVED_BY` /
  `XCPNG_AUDIT_RATIONALE` are optional annotations recorded on the audit row,
  never required.
- Budget guard: `XCPNG_MAX_TOOL_CALLS` (default ceiling on calls per process)
  and `XCPNG_MAX_TOOL_SECONDS` (cumulative wall-time), plus a runaway breaker
  for tight poll loops.
- No outbound traffic except the configured XO endpoint. No telemetry.

## MCP client setup

```json
{
  "mcpServers": {
    "xcpng-aiops": {
      "command": "uvx",
      "args": ["--from", "xcpng-aiops", "xcpng-aiops-mcp"],
      "env": { "XCPNG_AIOPS_MASTER_PASSWORD": "your-master-password" }
    }
  }
}
```

MCP clients do **not** inherit your shell environment — the master password
(and any `XCPNG_*` overrides) must be in the `env` block.
