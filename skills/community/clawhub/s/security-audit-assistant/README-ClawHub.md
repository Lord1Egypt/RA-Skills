# ClawHub Release Checklist - Security Audit Assistant

## ✅ Pre-Release

- [x] SKILL.md (formatted, includes pricing)
- [x] scripts/audit.js (functional, ~150 lines)
- [x] references/ (CIS summary)
- [x] README.md (user quick start)
- [ ] Test on Ubuntu 20.04+ (if available)
- [ ] Test on CentOS 8+ (if available)
- [ ] Verify OpenClaw skill manifest (if separate)

## 📸 Assets Needed

- [ ] Skill icon (512x512 PNG, transparent)
- [ ] Screenshot of sample output (example-report.txt)
- [ ] Demo video (optional, 60s)

## 📝 Metadata for ClawHub Submission

```
Name: Security Audit Assistant
Short description: Automated security baseline checks for OpenClaw nodes. Get CIS-inspired reports in seconds.
Full description: (from SKILL.md intro + features)
Category: System & Infrastructure
Tags: security, audit, compliance, ssh, firewall, cis
Price: $29/month
Trial: 7 days free
Supported OS: Ubuntu 20.04+, Debian 11+, CentOS 8+
```

## 🚀 Submission Steps

1. Zip the skill directory:
   ```bash
   zip -r security-audit-assistant-v1.0.zip skills/security-audit-assistant/
   ```

2. Upload to ClawHub:
   - Log in to https://clawhub.com (or OpenClaw dashboard → Marketplace)
   - Click "Submit Skill"
   - Fill form + upload zip
   - Agree to terms (70-80% revenue share)

3. Wait for review (1-3 business days)

4. Once approved:
   - Get shareable link
   - Announce on Discord/forums
   - Update MEMORY.md with launch date & link

## 📈 Post-Launch Tasks

- [ ] Monitor downloads (ClawHub analytics)
- [ ] Collect first 5 user reviews
- [ ] Iterate based on feedback (v1.1 within 2 weeks)
- [ ] Publish third skill (Security Audit Assistant is #2 of 3)

---

**Revenue Goal**: $200-500 MRR within 3 months (10-20 customers)
