---
name: security-auditor
description: Run security audits on Linux servers, web applications, and cloud infrastructure. Checks SSH hardening, firewall rules, open ports, SSL/TLS config, file permissions, and common vulnerabilities. Produces actionable reports.
metadata:
  version: 1.0.0
  author: TKDigital
  category: DevOps & Security
  tags: [security, audit, linux, hardening, vulnerability, devops, server]
---

# Security Auditor Skill

Comprehensive security auditing for Linux servers, web apps, and cloud infrastructure.

## What It Does

1. **Server Hardening Audit** — SSH config, firewall rules, user permissions, kernel parameters
2. **Port & Service Scan** — Open ports, running services, unnecessary exposure
3. **SSL/TLS Analysis** — Certificate validity, protocol versions, cipher suites
4. **File Permission Check** — World-readable configs, SUID binaries, sensitive file exposure
5. **Update Status** — Pending security patches, EOL software detection
6. **Web App Security** — Headers, CORS, cookie flags, common misconfigs
7. **Report Generation** — Prioritized findings with fix commands

## Usage

### Full Server Audit
```
Run a full security audit on this server.
Check: SSH, firewall, ports, users, file permissions, updates, SSL.
Output a prioritized report with fix commands.
```

### Quick SSH Hardening Check
```
Audit SSH configuration:
- Is root login disabled?
- Is password auth disabled?
- What port is it on?
- Are there any weak ciphers?
Give me the exact commands to fix any issues.
```

### Web Application Security Check
```
Check security headers and configuration for: [URL]
Look for:
- Missing security headers (CSP, HSTS, X-Frame-Options)
- SSL/TLS issues
- CORS misconfig
- Cookie security flags
- Information disclosure
```

### Cloud Infrastructure Review
```
Review my cloud setup for security issues:
- Provider: [AWS/GCP/DO/Vultr]
- Services: [list running services]
- Access: [how you connect]
Focus on: IAM, network exposure, storage permissions, logging
```

## Output Format

```
# Security Audit Report — [Target]
**Date**: [Audit date]
**Scope**: [What was audited]
**Risk Level**: [Critical/High/Medium/Low]

## 🔴 Critical Findings
### [Finding Title]
- **Risk**: [What could happen]
- **Current State**: [What's wrong]
- **Fix**: 
  ```bash
  [Exact command to fix]
  ```
- **Verification**: [How to confirm the fix worked]

## 🟡 Warnings
[Medium-risk findings]

## 🟢 Passed Checks
[What's already good]

## Summary
- Critical: [X]
- Warnings: [X]  
- Passed: [X]
- Overall Score: [X/100]
```

## Checks Performed

### SSH (12 checks)
- Root login status
- Password authentication
- Port configuration
- Key-based auth enforcement
- Protocol version
- Cipher suite strength
- MaxAuthTries setting
- LoginGraceTime
- AllowUsers/AllowGroups
- Banner configuration
- Idle timeout
- X11 forwarding

### Firewall (8 checks)
- UFW/iptables active
- Default deny policy
- Unnecessary open ports
- Rate limiting rules
- ICMP handling
- IPv6 rules
- Logging enabled
- Fail2ban status

### System (10 checks)
- Pending security updates
- EOL software
- SUID/SGID binaries
- World-writable files
- Unowned files
- Cron job permissions
- tmp/var/tmp permissions
- Kernel hardening (sysctl)
- Core dumps disabled
- Automatic updates configured

### Web/SSL (8 checks)
- Certificate validity/expiry
- Protocol versions (TLS 1.2+)
- Cipher suite strength
- HSTS header
- Content Security Policy
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy

## References

- `references/hardening-checklist.md` — Complete hardening checklist
- `references/common-fixes.md` — Copy-paste fix commands for common issues
