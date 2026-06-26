---
name: openclaw-security
version: 1.0.2
description: |
  ⚠️ HIGH PRIVILEGE SECURITY AUDIT SKILL
  
  Performs comprehensive security auditing for OpenClaw deployments. Requires system-level
  access for legitimate security scanning purposes. All operations are read-only and local-only.
  
  Covers: environment isolation, privilege checks, port exposure, skill trust sources, 
  version checks, process monitoring, sensitive directory changes, cron jobs, SSH audits, 
  file integrity baselines, yellow-line operation audits, disk usage, environment variable 
  leak detection, DLP scanning (private key/mnemonic detection), skill/MCP integrity tracking, 
  and disaster recovery backups.
  
  Use when: security audits, firewall/SSH/update hardening, risk posture review, exposure 
  assessment, or periodic security checks on machines running OpenClaw (laptop, workstation, 
  Pi, VPS).
---

# OpenClaw Security Audit

Comprehensive security auditing for OpenClaw deployments. This skill performs automated security checks and generates reports.

> **⚠️ Security Notice**: This skill requires elevated system access for legitimate security auditing purposes. See [SECURITY.md](./SECURITY.md) for detailed security declarations and data handling policies.

## Quick Start

Run the security audit script:

```bash
python3 scripts/openclaw_security_audit.py
```

This generates:
- **Brief summary** printed to stdout
- **Detailed report** saved to `/tmp/openclaw-security-reports/report-{DATE}.txt`

## What It Checks

| Check | Description |
|-------|-------------|
| Environment Isolation | Detects Docker/container/VM environments |
| Privilege Check | Verifies OpenClaw isn't running as root |
| Port Exposure | Checks if Gateway port 18789 is exposed |
| Skill Trust | Lists installed skills and their sources |
| Version Check | Compares current vs latest OpenClaw version |
| Process & Network | Captures listening ports and top processes |
| Sensitive Directories | Counts file changes in /etc, ~/.ssh, etc. |
| System Cron | Lists system timers and cron jobs |
| OpenClaw Cron | Retrieves internal OpenClaw scheduled tasks |
| SSH Audit | Recent logins and failed SSH attempts |
| File Integrity | SHA256 hash and permission checks |
| Yellow Line Audit | Compares sudo logs with memory records |
| Disk Usage | Root partition usage and large files |
| Environment Variables | Scans Gateway process for sensitive vars |
| DLP Scan | Detects plaintext private keys/mnemonics (read-only) |
| Skill/MCP Integrity | Tracks file hash changes over time |
| Disaster Recovery | Auto-commits OpenClaw state to Git (opt-in) |

## Security & Privacy

### Data Handling
- **All scans are local-only** - No data leaves your machine
- **Read-only operations** - No system modifications (except opt-in features)
- **Opt-in external features** - Git backup and Telegram notifications are disabled by default

### Sensitive Operations
See [SECURITY.md](./SECURITY.md) for detailed explanations of:
- DLP scanning (private key/mnemonic detection)
- Environment variable auditing
- Git disaster recovery

### Required Permissions
This skill requires system access for:
- Running system commands (`ss`, `top`, `systemctl`, etc.)
- Reading OpenClaw configuration files
- Inspecting Gateway process environment
- Scanning workspace files for credential leaks

## Output Format

### Brief Format (stdout)
```
OpenClaw Daily Security Brief (2026-03-11)

[OK] Environment Isolation: Running in isolated environment
[OK] Privilege Check: Complies with least privilege principle
[WARNING] Port Exposure: Port 18789 listening on all interfaces, recommend binding to 127.0.0.1
...

Warning Items:
[WARNING] Port Exposure: Port 18789 listening on all interfaces, recommend binding to 127.0.0.1
```

### Detailed Report
Full report saved to `/tmp/openclaw-security-reports/report-{DATE}.txt`

## Configuration

### Optional Features (Disabled by Default)

To enable external operations, set the following environment variables:

#### Git Disaster Recovery
```bash
export SECURITY_AUDIT_ENABLE_GIT=1
```
Enables automatic Git commit and push of OpenClaw state to your configured remote.

#### Telegram Notifications
```bash
export SECURITY_AUDIT_ENABLE_TELEGRAM=1
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"
```
Sends audit summary to Telegram after each run.

### Scheduling

To run daily via OpenClaw cron:
```bash
openclaw cron add --name "daily-security-audit" --schedule "0 9 * * *" --command "python3 ~/.openclaw/workspace/skills/openclaw-security/scripts/openclaw_security_audit.py"
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.2 | 2026-03-16 | Made Git backup and Telegram opt-in features (disabled by default) |
| 1.0.1 | 2026-03-16 | Added SECURITY.md, enhanced documentation |
| 1.0.0 | 2026-03-13 | Initial release |
