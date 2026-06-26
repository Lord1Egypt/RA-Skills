# Security Declaration

This skill performs legitimate security auditing functions for OpenClaw deployments.

## Required Privileges

This skill requires the following system access to perform comprehensive security audits:

- **System command execution**: `ss`, `top`, `systemctl`, `journalctl`, `last`, `df`, `find`
- **File system read access**: Scanning OpenClaw workspace, config files, and system directories
- **Process inspection**: Reading OpenClaw Gateway process environment variables
- **Network inspection**: Checking listening ports and network configuration

## Sensitive Operations Explained

### DLP (Data Loss Prevention) Scanning

**Purpose**: Detect accidentally committed private keys and mnemonic phrases in workspace files.

**Behavior**:
- **Read-only**: Only scans file content, never modifies
- **Local-only**: Scans only `~/.openclaw/workspace/` directory
- **Pattern matching**: Uses regex to detect Ethereum private keys (`0x[64 hex chars]`) and BIP-39 mnemonics
- **No exfiltration**: Results are stored locally only

### Environment Variable Audit

**Purpose**: Detect potential credential leaks in OpenClaw Gateway process.

**Behavior**:
- Reads `/proc/{pid}/environ` of the Gateway process only
- Only scans for sensitive variable **names** (SECRET, TOKEN, PASSWORD, KEY)
- Actual values are hidden/replaced with `(hidden)` in reports
- No credentials are logged or transmitted

### Git Disaster Recovery (Opt-in)

**Purpose**: Backup OpenClaw state to prevent data loss.

**Status**: **Disabled by default** - requires `SECURITY_AUDIT_ENABLE_GIT=1`

**Behavior**:
- Only operates on user's own `~/.openclaw/` Git repository
- Commits and pushes to user-configured remote only
- No external servers are contacted
- Must be explicitly enabled via environment variable

## Data Handling

| Aspect | Policy |
|--------|--------|
| Transmission | All scans are **local-only** |
| External Communication | Only opt-in features (Git push, Telegram) - disabled by default |
| Report Storage | `/tmp/openclaw-security-reports/` only |
| Retention | Reports are not automatically deleted, user-managed |
| Privacy | No personal data is collected or transmitted |

## Security Guarantees

1. **No data exfiltration**: This skill does not send any scanned data to external servers
2. **Read-only by default**: Core scans are read-only; external features (Git, Telegram) are disabled by default
3. **Transparent**: All operations are logged in generated reports
4. **User-controlled**: All external operations require explicit opt-in via environment variables

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Credential exposure in reports | Sensitive values are masked as `(hidden)` |
| Unauthorized Telegram notifications | Requires `SECURITY_AUDIT_ENABLE_TELEGRAM=1` AND bot token/chat ID |
| Unauthorized Git operations | Requires `SECURITY_AUDIT_ENABLE_GIT=1` AND existing Git repo with user-configured remote |
| Privilege escalation | Script checks and warns if running as root |
| Data leakage via Git | Only pushes to user-configured remote |

## Compliance

This skill is designed for:
- Personal security auditing of your own OpenClaw deployment
- Compliance with security best practices
- Proactive detection of misconfigurations and credential leaks

It is **NOT** designed for:
- Unauthorized access to systems you don't own
- Data exfiltration
- Malicious surveillance

---

**Version**: 1.0.2  
**Last Updated**: 2026-03-16  
**Audit Frequency**: Recommended daily via cron
