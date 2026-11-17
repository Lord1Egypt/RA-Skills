# veeam-aiops setup guide

## Install

```bash
uv tool install veeam-aiops
# or: pipx install veeam-aiops
```

## Configure (recommended: the wizard)

```bash
veeam-aiops init            # collects connection details + an encrypted password
veeam-aiops doctor          # verifies config, encrypted store, connectivity
```

`init` writes `~/.veeam-aiops/config.yaml` (no secrets) and stores the login
password **encrypted** in `~/.veeam-aiops/secrets.enc` (Fernet + scrypt; chmod
600). It prompts for a *master password* that unlocks the store; set it via
`VEEAM_AIOPS_MASTER_PASSWORD` for non-interactive (MCP/CI) use.

Example `~/.veeam-aiops/config.yaml`:

```yaml
targets:
  - name: vbr-lab
    host: 10.0.0.20
    username: "DOMAIN\\backup-admin"   # or a local account on the VBR server
    port: 9419                          # Veeam REST API port (default)
    verify_ssl: false                   # self-signed lab certs only; true in prod
```

### Manage credentials manually

```bash
veeam-aiops secret set vbr-lab         # prompts hidden for the password
veeam-aiops secret list                # names only; values never shown
veeam-aiops secret rotate-password     # re-encrypt under a new master password
veeam-aiops secret migrate             # import a legacy plaintext .env, then archives it
```

Secret names map to target names. A legacy plaintext env var
`VEEAM_<TARGET_NAME_UPPER>_PASSWORD` is still honoured as a fallback (with a
deprecation warning) — `secret migrate` imports it into the encrypted store.

## Use as an MCP server

```jsonc
{
  "command": "veeam-aiops",
  "args": ["mcp"],
  "env": {
    "VEEAM_AIOPS_CONFIG": "~/.veeam-aiops/config.yaml",
    "VEEAM_AIOPS_MASTER_PASSWORD": "your-master-password"
  }
}
```

`VEEAM_AIOPS_MASTER_PASSWORD` lets the server unlock `secrets.enc` without an
interactive prompt.

Using the `veeam-aiops mcp` subcommand (rather than `uvx --from`) means the MCP
client launches the already-installed entry point and does not re-resolve the
package over the network at startup.

## Security

> **Disclaimer**: Community-maintained project, **not affiliated with, endorsed
> by, or sponsored by Veeam Software**. MIT licensed. See `SECURITY.md`.

- **Credentials**: stored **encrypted** in `~/.veeam-aiops/secrets.enc`
  (Fernet/AES-128 + scrypt-derived key, chmod 600) — never plaintext on disk.
  The master password is never stored (only a per-store salt + ciphertext) and
  comes from `VEEAM_AIOPS_MASTER_PASSWORD` or an interactive prompt. The login
  password is exchanged for a short-lived OAuth2 bearer token at connect time
  and kept only in memory.
- **Audit**: every operation logged to a local SQLite DB under
  `~/.veeam-aiops/` (relocate with `VEEAM_AIOPS_HOME`).
- **Budget guard**: cap calls/wall-time with `VEEAM_MAX_TOOL_CALLS` /
  `VEEAM_MAX_TOOL_SECONDS`; a runaway session-poll/retry loop trips automatically.
- **Risk tier**: a descriptive label recorded on each audit row (derived from
  `risk_level`); it gates nothing. `VEEAM_AUDIT_APPROVED_BY` /
  `VEEAM_AUDIT_RATIONALE` are optional annotations recorded alongside it.
- **Destructive ops**: `job stop`, `session stop`, and `restore start` require
  double confirmation + support `--dry-run` at the CLI.
- **TLS**: `verify_ssl` defaults true; disable only for self-signed labs.
- **No webhooks / telemetry / background services.**

## Least privilege

Create a dedicated Veeam Backup & Replication user with only the role your
workflows need (e.g. a restricted backup-operator role) rather than a full
administrator account.
