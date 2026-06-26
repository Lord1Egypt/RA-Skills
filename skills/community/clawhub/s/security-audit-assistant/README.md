# Security Audit Assistant

> Automated security baseline checks for OpenClaw nodes

Quick 7-day trial. No credit card required.

---

## 🚀 Installation

1. Open ClawHub and search "Security Audit Assistant"
2. Click "Install" (one-click)
3. Done - skill appears in your OpenClaw CLI

---

## ⚡ First Audit

```bash
# Check all your managed nodes
openclaw skill run security-audit-assistant --all

# Check a specific server
openclaw skill run security-audit-assistant --node web-01

# Get JSON output (for integrations)
openclaw skill run security-audit-assistant --format json > audit.json
```

---

## 📋 What's Included

- ✅ SSH hardening checks (password auth, root login, protocol)
- ✅ Firewall status (UFW/firewalld)
- ✅ Security updates availability
- ✅ Password aging policies
- ✅ Auditd & rsyslog validation
- ✅ Critical file permissions
- ✅ ~20 total checks

**Takes ~8 seconds per node.**

---

## 💡 Sample Workflow

```bash
# 1. Run audit
openclaw skill run security-audit-assistant --all

# 2. Review output (see FAIL items)
# 3. Copy fix commands from report
# 4. Execute fixes (one-liners provided)
# 5. Re-run to verify
```

---

## ⏰ Automate Weekly Audits

```bash
# Add cron to run every Sunday at 2 AM
openclaw cron add --expr "0 2 * * 0" "openclaw skill run security-audit-assistant --all"
```

Reports will be logged automatically. Add email forwarding via OpenClaw notifications.

---

## 🆘 Need Help?

- **Documentation**: `references/cis-benchmark-summary.md`
- **Report Issues**: https://github.com/your-username/security-audit-assistant/issues
- **Support Email**: support@your-domain.com

---

## 💰 Pricing

- **$29/month** per OpenClaw instance (unlimited nodes)
- **First 7 days free**

*Cancel anytime from ClawHub dashboard.*

---

## 🔒 Privacy

- All scans run locally on your infrastructure
- No data sent to external servers
- Zero telemetry beyond error reports (opt-in)

---

**Ready?** `openclaw skill install security-audit-assistant`
