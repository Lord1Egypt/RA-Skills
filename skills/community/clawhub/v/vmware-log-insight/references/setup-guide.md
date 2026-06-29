# vmware-log-insight Setup Guide

## Install

```bash
uv tool install vmware-log-insight
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
default_target: prod
```

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
reachability (TCP 9543), authentication, appliance version, and MCP server import.

## MCP client configuration

```json
{
  "command": "uvx",
  "args": ["--from", "vmware-log-insight", "vmware-log-insight-mcp"],
  "env": { "VMWARE_LOG_INSIGHT_CONFIG": "~/.vmware-log-insight/config.yaml" }
}
```

If you installed with `uv tool install`, prefer the entry point `vmware-log-insight mcp`
(no PyPI resolution at startup — robust behind corporate TLS proxies, 踩坑 #25).

## Security

> **Disclaimer**: Community-maintained open-source project, **not affiliated with,
> endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.**

1. **Source Code** — https://github.com/zw008/VMware-Log-Insight (MIT).
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
