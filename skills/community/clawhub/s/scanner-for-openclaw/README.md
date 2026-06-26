# OpenClaw Security Scanner

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-%3E%3D2026.3.0-green.svg)](https://github.com/openclaw/openclaw)
[![ClawHub](https://img.shields.io/badge/ClawHub-available-orange.svg)](https://clawhub.com)

**Security Expert for OpenClaw Deployments**

Comprehensive security auditing for OpenClaw with safe remediation guidance.

## Features

- 🔍 **Network Security Scan** - Detect exposed ports, default configs
- 📱 **Channel Policy Audit** - Check Telegram, WhatsApp, Web security
- 🔐 **Permission Analysis** - Evaluate tool execution and filesystem access
- 🛡️ **Safe Remediation** - Risk-assessed fixes with rollback plans

## Installation

### Via ClawHub (Recommended)

```bash
# Install from registry
clawhub install openclaw-security-scanner

# Verify
clawhub list | grep security-scanner
```

### Manual Installation

```bash
# Clone to skills directory
git clone https://github.com/openclaw/openclaw.git
cp -r openclaw/skills/openclaw-security-scanner ~/.openclaw/workspace/skills/

# Validate
python3 ~/.openclaw/workspace/skills/skill-creator/scripts/quick_validate.py openclaw-security-scanner
```

### Requirements

- OpenClaw >= 2026.3.0, Python 3.8+
- **Optional**: `lsof` or `ss` (iproute2) for port binding detection

## Quick Start

```bash
# Full security audit
openclaw security-scan

# Save report
openclaw security-scan -o security_report.md

# Targeted scans
openclaw security-scan --ports-only
openclaw security-scan --channels
openclaw security-scan --permissions
```

## Usage

### Basic Scan

```bash
openclaw security-scan
```

Output:
```
[INFO] OpenClaw Security Scanner v1.0.0
[INFO] ============================================================
[1/3] Network port scanning...
[2/3] Channel policy audit...
[3/3] Permission analysis...
[INFO] Scan complete. 5 findings.

Risk Level: HIGH
Report saved to: security_report_20260308_163000.md
```

### Generate Report

```bash
openclaw security-scan --output report.md --verbose
```

## Risk Levels

| Level | Response | Examples |
|-------|----------|----------|
| 🔴 CRITICAL | < 1 hour | Exposed admin port, allow-all policies |
| 🟠 HIGH | < 24 hours | Missing auth, excessive permissions |
| 🟡 MEDIUM | < 1 week | Weak rate limiting, verbose errors |
| 🔵 LOW | < 1 month | Missing headers, suboptimal logging |

## Safety First

⚠️ **Golden Rule**: Never apply fixes that may break remote access without:

1. ✅ Verified backup access (SSH, console)
2. ✅ Config backup
3. ✅ Rollback plan ready

Every finding includes:
- Risk assessment
- Impact description
- Remediation steps
- **Risk of fix** (will this break things?)
- **Rollback plan**

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/security_scan.py` | Main scanner |
| `scripts/cli.py` | CLI wrapper |

## References

- `references/permission-management.md` - Context-aware permissions
- `references/remediation-playbook.md` - Safe fix procedures

## Examples

### Weekly Security Check

Add to `HEARTBEAT.md`:
```markdown
Sunday 02:00:
- Run: `openclaw security-scan -o weekly_security.md`
- Review CRITICAL/HIGH findings
```

### Check Telegram Safety

```bash
openclaw security-scan --channels --output telegram_audit.md
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests
4. Submit PR

## License

MIT License - See [LICENSE](LICENSE) for details.

---

**Version**: 1.0.2
**Updated**: 2026-03-09  
**Maintainer**: DTClaw Team
