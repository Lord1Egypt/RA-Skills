---
name: security-plus
description: "Enhanced security with OWASP Top 10, dependency scanning, SAST/DAST, secrets detection, compliance checks, and security hardening guides."
metadata:
  author: opencode
  version: 2.0
  tags: security, owasp, vulnerability-scanning, compliance, hardening
  compatibility: opencode
  license: MIT
---

# Security Plus

Enhanced security with OWASP Top 10, vulnerability scanning, and compliance checks.

## Features

- **OWASP Top 10**: Complete coverage of web application risks
- **Vulnerability Scanning**: SAST, DAST, dependency scanning
- **Secrets Detection**: Prevent credential leaks
- **Compliance Checks**: GDPR, HIPAA, SOC2 basics
- **Security Hardening**: Server, application, database hardening

## Quick Reference

| Risk | Category | Mitigation |
|------|----------|------------|
| Injection | A03:2021 | Parameterized queries |
| Broken Auth | A07:2021 | MFA, secure session |
| XSS | A03:2021 | Input validation, output encoding |
| SSRF | A10:2021 | Input validation, allowlists |
| Security Misconfig | A05:2021 | Secure defaults, hardening |

## OWASP Top 10 (2021)

### A01: Broken Access Control

```markdown
# Prevention
- Deny by default
- Implement RBAC/ABAC
- Validate permissions server-side
- Log access control failures
- Rate limit API access
```

### A02: Cryptographic Failures

```markdown
# Prevention
- Use strong algorithms (AES-256, RSA-2048+)
- Never store passwords in plaintext
- Use bcrypt/argon2 for password hashing
- Encrypt data at rest and in transit
- Manage keys properly
```

### A03: Injection

```markdown
# Prevention
- Use parameterized queries
- Validate and sanitize input
- Use ORM/ODM libraries
- Escape output
- Use LIMIT and other SQL controls
```

### A04: Insecure Design

```markdown
# Prevention
- Threat modeling
- Secure design patterns
- Reference architecture
- Security requirements
- Secure development lifecycle
```

### A05: Security Misconfiguration

```markdown
# Prevention
- Secure defaults
- Minimal installation
- Review configurations
- Automated verification
- Hardening guides
```

### A06: Vulnerable Components

```markdown
# Prevention
- Dependency scanning
- Automated updates
- Software composition analysis
- Monitor CVEs
- Remove unused dependencies
```

### A07: Authentication Failures

```markdown
# Prevention
- Multi-factor authentication
- Secure password storage
- Rate limiting
- Session management
- Account lockout
```

### A08: Software and Data Integrity

```markdown
# Prevention
- Digital signatures
- CI/CD pipeline security
- Dependency verification
- Code review
- Integrity checks
```

### A09: Security Logging Failures

```markdown
# Prevention
- Log security events
- Centralized logging
- Alert on suspicious activity
- Log integrity protection
- Incident response plan
```

### A10: Server-Side Request Forgery

```markdown
# Prevention
- Input validation
- URL allowlists
- Disable HTTP redirections
- Segment networks
- Use metadata endpoints
```

## Vulnerability Scanning

### SAST (Static Application Security Testing)

```bash
# SonarQube
sonar-scanner

# Semgrep
semgrep scan --config=auto

# Bandit (Python)
bandit -r src/
```

### DAST (Dynamic Application Security Testing)

```bash
# OWASP ZAP
docker run -t owasp/zap2docker-stable zap-baseline.py -t https://example.com

# Nikto
nikto -h https://example.com
```

### Dependency Scanning

```bash
# npm audit
npm audit
npm audit fix

# Snyk
npx snyk test
npx snyk monitor

# Safety (Python)
safety check

# Bundler-audit (Ruby)
bundle-audit check --update
```

## Secrets Detection

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Add to .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

### Scanning Tools

```bash
# detect-secrets
detect-secrets scan

# gitleaks
gitleaks detect --source . --verbose

# truffleHog
trufflehog git file://. --only-verified
```

### Secret Patterns

```markdown
# Common patterns to detect
- AWS keys: AKIA[0-9A-Z]{16}
- GitHub tokens: gh[pousr]_[A-Za-z0-9]{36}
- Private keys: -----BEGIN.*PRIVATE KEY-----
- API keys: [a-zA-Z0-9]{32,}
- Passwords: password\s*[:=]\s*[^\s]+
```

## Compliance Checks

### GDPR

```markdown
# Requirements
- Data minimization
- Purpose limitation
- Storage limitation
- Right to erasure
- Data portability
- Consent management
```

### HIPAA

```markdown
# Requirements
- Access controls
- Audit controls
- Integrity controls
- Transmission security
- Encryption at rest
- Business associate agreements
```

### SOC2

```markdown
# Trust Service Criteria
- Security
- Availability
- Processing integrity
- Confidentiality
- Privacy
```

## Security Hardening

### Server Hardening

```markdown
# SSH
- Disable root login
- Use key-based auth
- Change default port
- Limit SSH users

# Firewall
- Allow only necessary ports
- Rate limit connections
- Block known malicious IPs

# Updates
- Enable automatic security updates
- Remove unused packages
- Disable unnecessary services
```

### Application Hardening

```markdown
# Headers
- Content-Security-Policy
- X-Content-Type-Options
- X-Frame-Options
- Strict-Transport-Security

# Cookies
- Secure flag
- HttpOnly flag
- SameSite attribute
- Short expiration

# Input Validation
- Whitelist validation
- Length limits
- Type checking
- Sanitization
```

### Database Hardening

```markdown
# Access
- Least privilege
- Separate accounts
- Strong passwords
- Network restrictions

# Configuration
- Disable remote access
- Enable encryption
- Audit logging
- Regular backups

# Queries
- Parameterized queries
- Input validation
- Output encoding
```

## Security Checklist

### Development

- [ ] Security requirements defined
- [ ] Threat modeling completed
- [ ] Secure coding guidelines followed
- [ ] Code review for security
- [ ] Dependencies scanned

### Deployment

- [ ] Secure configuration
- [ ] Secrets in vault
- [ ] HTTPS enabled
- [ ] Security headers set
- [ ] Logging configured

### Operations

- [ ] Monitoring enabled
- [ ] Alerts configured
- [ ] Incident response plan
- [ ] Regular audits
- [ ] Backup testing

## Tools Reference

| Category | Tool | Purpose |
|----------|------|---------|
| SAST | SonarQube, Semgrep | Code analysis |
| DAST | OWASP ZAP, Nikto | Runtime testing |
| Dependencies | Snyk, npm audit | Vulnerability scanning |
| Secrets | detect-secrets, gitleaks | Credential detection |
| Container | Trivy, Clair | Image scanning |
| Infrastructure | Checkov, tfsec | IaC scanning |

## Best Practices

1. **Shift left** - Security early in development
2. **Defense in depth** - Multiple security layers
3. **Least privilege** - Minimal permissions
4. **Secure defaults** - Out-of-box security
5. **Fail securely** - Graceful degradation
6. **Don't trust input** - Validate everything
7. **Log security events** - Audit trail
8. **Regular updates** - Patch vulnerabilities
