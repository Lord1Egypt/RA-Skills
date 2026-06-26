---
name: openclaw-security-scanner
version: 1.0.4
slug: openclaw-security-scanner
description: |
  Security expert for OpenClaw deployments. Audits local configuration files for
  vulnerabilities in network settings, channel policies, and tool permissions.
  Pure static analysis — no network probing, no subprocess execution, no system
  command calls. Provides safe remediation with rollback plans.
homepage: https://github.com/openclaw/openclaw/tree/main/skills/openclaw-security-scanner
changelog: |
  1.0.4 - Fix typo errors 
  1.0.3 - Pure config-based static analysis (no risky capabilities)
    - Removed all subprocess calls (lsof, ss, openclaw CLI)
    - Removed all network socket connections (port probing)
    - Scan now performs pure config-file static analysis only
    - Added TLS/SSL configuration check
    - Added bind-address-missing warning
    - CLI wrapper calls scanner directly instead of via subprocess
    - Resolves ClawHub suspicious classification
  1.0.2 - Remove external network access
    - Removed GitHub API fetching to eliminate outbound HTTP requests
    - Scan now operates fully offline on local configuration only
  1.0.0 - Initial release
    - Network port scanning (exposed ports, default ports, binding config)
    - Channel policy audit (Telegram, WhatsApp, Web authentication)
    - Permission analysis (tool exec, filesystem access)
    - Safe remediation playbook with rollback procedures
    - Context-aware permission management guide
license: MIT
author: DTClaw Team <dtclaw@163.com>
tags:
  - security
  - audit
  - scanner
  - hardening
  - compliance
minOpenClawVersion: 2026.3.0
---

# OpenClaw Security Scanner

**Role**: Security Expert for OpenClaw Deployments

**Purpose**: Audit OpenClaw configuration files for security vulnerabilities and provide safe, actionable remediation guidance. Pure static analysis — reads local config files only, no network probing, no subprocess execution.

## Installation

### Via ClawHub (Recommended)

```bash
# Install from ClawHub registry
clawhub install openclaw-security-scanner

# Or install from local workspace
clawhub install skills/openclaw-security-scanner

# Verify installation
clawhub list | grep security-scanner
```

### Manual Installation

```bash
# Clone or copy to skills directory
cp -r openclaw-security-scanner ~/.openclaw/workspace/skills/

# Validate installation
python3 ~/.openclaw/workspace/skills/skill-creator/scripts/quick_validate.py openclaw-security-scanner
```

### Requirements

- OpenClaw >= 2026.3.0
- Python 3.8+
- No external tools required — all analysis is based on local config files

## Quick Start

After installation, run a security scan:

```bash
# Full security audit (recommended)
openclaw security-scan

# Or use the Python script directly
python3 skills/openclaw-security-scanner/scripts/security_scan.py

# Generate report to file
openclaw security-scan --output security_report.md
```

## When to Use

Trigger this skill when:
- User requests security audit: "scan my OpenClaw for security issues"
- After initial setup to verify security posture
- Before exposing OpenClaw to production/multi-user environments
- After major configuration changes
- Periodic security health checks (recommended: weekly)
- User reports suspicious activity

## Commands

The skill provides these commands via `openclaw` CLI:

| Command | Description | Example |
|---------|-------------|---------|
| `security-scan` | Full security audit | `openclaw security-scan` |
| `security-scan --ports-only` | Analyze network config only | `openclaw security-scan --ports-only` |
| `security-scan --channels` | Audit channel policies | `openclaw security-scan --channels` |
| `security-scan --permissions` | Analyze permissions | `openclaw security-scan --permissions` |
| `security-scan --output FILE` | Save report to file | `openclaw security-scan -o report.md` |

## Features

### 1. Network Configuration Analysis

Analyzes gateway config for:
- Bind address settings (0.0.0.0 vs 127.0.0.1)
- Default/predictable port usage
- TLS/SSL configuration
- Missing bind address declarations

**Example Output**:
```
🔴 CRITICAL: Gateway configured to bind to all interfaces (0.0.0.0:18789)
   Impact: Attackers on the network can access gateway API
   Fix: Set bind address to 127.0.0.1 or use firewall rules
   Risk: MEDIUM - may break remote access if not careful
```

### 2. Channel Policy Audit

Checks:
- Telegram `groupPolicy` (allow vs allowlist)
- WhatsApp webhook secrets
- Web channel authentication
- Group chat allowlists
- Unknown user policies

**Example Output**:
```
🔴 CRITICAL: Telegram allows all group messages
   Current: groupPolicy="allow"
   Impact: Anyone can send messages, potential for abuse
   Fix: Set groupPolicy="allowlist" and configure allowedGroups
   Risk: LOW - won't break 1:1 chats
```

### 3. Permission Analysis

Evaluates:
- Tool execution policy (allow vs deny vs allowlist)
- Filesystem access scope (workspaceOnly)
- Dangerous tools enabled (exec, shell, system.run)
- Context-aware permission configuration

**Example Output**:
```
🔴 CRITICAL: Tool execution policy is 'allow'
   Impact: Any tool can run arbitrary commands
   Fix: Set tools.exec.policy="deny" or "allowlist"
   Risk: HIGH - may break existing workflows
```

### 4. Safe Remediation

Every finding includes:
- **Risk Assessment**: CRITICAL/HIGH/MEDIUM/LOW
- **Impact Description**: What could go wrong
- **Remediation Steps**: How to fix
- **Risk of Fix**: LOW/MEDIUM/HIGH (will this break things?)
- **Rollback Plan**: How to undo if something goes wrong

## Risk Scoring

| Level | Response Time | Examples |
|-------|---------------|----------|
| 🔴 **CRITICAL** | < 1 hour | Exposed admin port, allow-all channel policy, default credentials |
| 🟠 **HIGH** | < 24 hours | Missing authentication, excessive tool permissions, no TLS |
| 🟡 **MEDIUM** | < 1 week | Weak rate limiting, verbose errors, outdated dependencies |
| 🔵 **LOW** | < 1 month | Missing security headers, suboptimal logging |

## Safe Remediation Protocol

All remediation steps in this skill are **configuration-file edits only**. The skill never executes system commands; any steps requiring service restarts or shell access are documented as **[OPERATOR]** actions for the human administrator.

⚠️ **CRITICAL RULE**: Never apply config changes that may break remote access without:

1. ✅ Verified backup access (SSH, console, secondary channel)
2. ✅ Config backup with tested restore procedure
3. ✅ Maintenance window scheduled
4. ✅ Rollback plan ready

### High-Risk Changes Require Staged Rollout

```
Phase 1: Preparation
├─ Copy config.json as backup
├─ Document current state
├─ [OPERATOR] Verify alternative access (SSH, console)
└─ Schedule maintenance window

Phase 2: Staging
├─ Apply config change to test environment
├─ Verify functionality
├─ Test rollback procedure
└─ Get approval

Phase 3: Production
├─ Apply config change during maintenance window
├─ [OPERATOR] Restart gateway and monitor (24-48 hours)
├─ Keep rollback ready
└─ Document changes

Phase 4: Verification
├─ Re-run scanner to verify improvement
├─ [OPERATOR] Test all critical functions
├─ [OPERATOR] Monitor for issues
└─ Update documentation
```

## Output Format

Reports are generated in Markdown format:

```markdown
# OpenClaw Security Audit Report

**Scan Date**: 2026-03-08 16:30
**Hostname**: mybot.local
**Overall Risk Level**: HIGH

## Executive Summary
- 🔴 CRITICAL: 2
- 🟠 HIGH: 3
- 🟡 MEDIUM: 5
- 🔵 LOW: 2

## Findings
[Detailed findings with remediation steps]

## Remediation Plan
### Immediate Actions (< 24h)
- [ ] Fix 1 (Risk: LOW)
- [ ] Fix 2 (Risk: MEDIUM)

### Staged Rollout Required
- [ ] Fix 3 (Risk: HIGH - may break remote access)
```

## Examples

### Basic Security Scan

User: "Scan my OpenClaw for security issues"

Assistant runs:
```bash
openclaw security-scan --output security_report.md
```

Output:
```
✅ Network config analysis: 2 issues found
✅ Channel audit: 1 unsafe policy found  
✅ Permission analysis: 3 excessive permissions

Risk Level: HIGH
Report saved to: security_report.md
```

### Targeted Channel Audit

User: "Check if my Telegram configuration is safe"

Assistant runs:
```bash
openclaw security-scan --channels --output telegram_audit.md
```

### Weekly Security Check

Add to `HEARTBEAT.md`:
```markdown
## Weekly Security Scan

Every Sunday at 02:00:
- Run: `openclaw security-scan -o weekly_security.md`
- Review CRITICAL/HIGH findings
- Apply low-risk fixes
- Report summary to admin channel
```

## Integration

### Heartbeat Integration

```yaml
# ~/.openclaw/workspace/HEARTBEAT.md
weekly_security_scan:
  schedule: "0 2 * * 0"  # Sunday 2 AM
  command: "openclaw security-scan -o docs/reports/weekly_security.md"
  review: "Within 24 hours"
```

### Alert Triggers

Configure alerts for:
- New CRITICAL findings
- Configuration drift from secure baseline
- Failed authentication attempts > 10/hour
- Unusual tool execution patterns

## Scripts

All scripts are located in `skills/openclaw-security-scanner/scripts/`:

| Script | Purpose | Usage |
|--------|---------|-------|
| `security_scan.py` | Main security scanner | `python3 security_scan.py [options]` |

### Script Options

```bash
# security_scan.py
--ports-only        Only analyze network configuration
--channels-only     Only audit channel policies
--permissions-only  Only analyze permissions
--output, -o FILE   Save report to file
--verbose, -v       Verbose output
--full              Full scan (default)
```

## References

Detailed guides in `skills/openclaw-security-scanner/references/`:

- **permission-management.md** - Context-aware permission configuration
  - Permission levels (Restricted/Standard/Elevated/Emergency)
  - User-based, channel-based, time-based contexts
  - Lifecycle management and approval workflows
  - Quick switch commands and profiles

- **remediation-playbook.md** - Safe fix procedures
  - Golden rules for safe remediation
  - Step-by-step fixes for common issues
  - Rollback procedures for every fix
  - Emergency recovery procedures
  - Post-mortem templates

## Troubleshooting

### Config Not Found

```
[WARN] No config file found
```

**Solution**: Ensure OpenClaw config exists at one of:
- `~/.openclaw/openclaw.json` (primary)
- `~/.openclaw/config.json`
- `~/.openclaw/gateway.config.json`
- `/etc/openclaw/openclaw.json`
- Or set the `OPENCLAW_CONFIG` environment variable to a custom path

### Permission Denied

```
Error: [Errno 13] Permission denied
```

**Solution**: Run with appropriate permissions or check file ownership.

## Safety Warnings

This skill only **reads** configuration files and **writes** a report. It does not modify configs, restart services, or execute system commands.

Remediation steps in the report and reference docs are **[OPERATOR]** actions — the human administrator applies them:

1. Always back up `config.json` before editing
2. Verify alternative access (SSH, console) before high-risk changes
3. Test changes in staging first
4. Keep rollback plan ready

## Limitations

- Config-only analysis — does not actively probe network ports or running processes
- Cannot scan network topology beyond host
- Cannot test physical security
- Cannot assess social engineering risks

## Support

For security emergencies:
1. Run full scan immediately
2. Apply CRITICAL fixes with rollback ready
3. Report findings to security team
4. Schedule follow-up audit in 7 days

## Contributing

To contribute improvements:
1. Fork the repository
2. Create feature branch
3. Add tests for new checks
4. Submit pull request

## License

MIT License - See LICENSE file for details.

---

**Skill Version**: 1.0.4
**Last Updated**: 2026-03-12  
**Maintainer**: Security Team  
**Contact**: security@openclaw.ai
