# Security Audit Assistant

**Type**: System Health & Security  
**Audience**: DevOps, Sysadmins, Small Business Owners  
**Price**: $29/month (ClawHub)  
**Tags**: security, compliance, audit, ssh, firewall, cis

---

## 🎯 What Problem Does This Solve?

Small teams and solopreneurs often run servers without dedicated security staff. They:
- Don't know if their SSH/Firewall configurations are secure
- Miss critical security updates
- Need compliance-like reports for clients or audits
- Want automated checks without installing heavy tools

This skill runs a **lightweight security baseline audit** on any OpenClaw-managed node, generates a human-readable report, and provides one-click fix commands.

---

## ✨ Key Features

1. **Zero-Install Scanning** - Uses native OpenClaw node access, no agents needed
2. **CIS-Inspired Checks** - Focus on high-impact items (SSH, firewall, updates, passwords)
3. **Natural Language Summary** - "You have 3 high-risk issues, 5 medium"
4. **Executable Fixes** - Each finding includes the exact CLI command to remediate
5. **Scheduled Audits** - Can be automated via OpenClaw cron
6. **Export Formats** - Markdown, JSON, or plain text

---

## 🚀 Quick Start

```bash
# Run full audit on all managed nodes
openclaw skill run security-audit-assistant --all

# Run audit on specific node
openclaw skill run security-audit-assistant --node my-server

# JSON output for integration
openclaw skill run security-audit-assistant --format json

# Schedule weekly audit (via OpenClaw cron)
openclaw cron add --expr "0 2 * * 0" "openclaw skill run security-audit-assistant --all"
```

---

## 📊 What Gets Checked?

| Category | Checks | Risk Level |
|----------|--------|------------|
| SSH | Password auth disabled, root login disabled, protocol 2 only | High |
| Firewall | UFW/iptables enabled, default deny, necessary ports open | High |
| Updates | Security updates available, last update < 30 days | Medium |
| Passwords | Password aging enabled, no default accounts | Medium |
| Services | Unnecessary services disabled (telnet, vsftpd) | Low |
| Logging | Auditd/rsyslog enabled and rotating | Medium |
| File Permissions | /etc/passwd, /etc/shadow correct perms | High |

**Total checks**: ~20 per node

---

## 📈 Sample Output

```
🔍 Security Audit Report - server-01 (2026-03-26)

✅ PASS: 12 checks
⚠️  WARN: 4 checks
❌ FAIL: 3 checks

❌ HIGH RISK:
1. SSH password authentication is ENABLED
   Fix: sudo sed -i 's/PasswordAuthentication yes/no/' /etc/ssh/sshd_config && sudo systemctl restart sshd

⚠️  MEDIUM:
2. Security updates available (5 packages)
   Fix: sudo apt update && sudo apt upgrade -y

✅ All checks completed in 8 seconds.
```

---

## 🔄 Integration Use Cases

- **Pre-sales compliance**: Show clients you take security seriously
- **Monthly health checks**: Automated via cron, email reports
- **Onboarding new servers**: Run immediately after provisioning
- **Client reports**: Export to PDF and include in monthly invoices

---

## 💰 Pricing & Value

- **Cost**: $29/month per OpenClaw instance (unlimited nodes)
- **Time saved**: ~2 hours/month per server (manual audit)
- **ROI**: 1 server pays for itself; 5+ servers = massive savings

---

## 🛠️ Technical Details

- **Script**: `scripts/audit.js` (~150 lines, Node.js)
- **Dependencies**: None (uses OpenClaw node.exec)
- **Compatible OS**: Ubuntu 20.04+, Debian 11+, CentOS 8+
- **Permissions**: Requires sudo for some checks (prompts user)

---

## 📞 Support

- Issues: https://github.com/your-username/security-audit-assistant/issues
- Documentation: See `references/cis-benchmark-summary.md`

---

## 🧪 Trial

First 7 days free. No credit card required.
