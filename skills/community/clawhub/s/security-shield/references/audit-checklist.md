# Security Audit Checklist

Use this for security assessments, penetration testing guidance, and hardening reviews.

---

## Quick Security Audit (15 minutes)

### Immediate Checks
```bash
# 1. Check for exposed secrets in code
git grep -i "api_key\|password\|secret\|token" -- "*.py" "*.js" "*.env"

# 2. Find world-writable files
find /path/to/project -perm -002 -type f

# 3. Check for hardcoded credentials
grep -r "sk-\|ghp_\|Bearer " --include="*.py" --include="*.js" .

# 4. Verify .gitignore excludes secrets
cat .gitignore | grep -E "\.env|secrets|keys"
```

---

## Web Application Security Checklist

### Authentication
- [ ] Password hashing (bcrypt, argon2, scrypt)
- [ ] Rate limiting on login endpoints
- [ ] Account lockout after failed attempts
- [ ] MFA available and encouraged
- [ ] Session timeout configured
- [ ] Secure cookie flags (HttpOnly, Secure, SameSite)

### Authorization
- [ ] Role-based access control (RBAC)
- [ ] Principle of least privilege
- [ ] IDOR prevention (validate ownership)
- [ ] Admin routes protected
- [ ] API scopes/permissions enforced

### Input Validation
- [ ] All user input validated
- [ ] SQL queries parameterized
- [ ] XSS prevention (escape output)
- [ ] File upload validation (type, size)
- [ ] Path traversal prevention
- [ ] Command injection prevention

### Network Security
- [ ] HTTPS enforced (HSTS header)
- [ ] TLS 1.2+ only
- [ ] Certificate pinning (mobile apps)
- [ ] CORS configured properly
- [ ] Security headers set:
  - Content-Security-Policy
  - X-Frame-Options
  - X-Content-Type-Options
  - Referrer-Policy

---

## Infrastructure Security Checklist

### Server Hardening
- [ ] OS security updates applied
- [ ] Unnecessary services disabled
- [ ] Firewall configured (deny-by-default)
- [ ] SSH key-only authentication
- [ ] Root login disabled (SSH)
- [ ] Fail2ban or similar installed
- [ ] Disk encryption enabled
- [ ] Backups configured and tested

### Container Security (if applicable)
- [ ] Minimal base images (alpine, distroless)
- [ ] Non-root user in containers
- [ ] Secrets via env vars or vault (not baked in)
- [ ] Image scanning enabled
- [ ] Resource limits set (CPU, memory)
- [ ] Network policies configured

### Database Security
- [ ] Strong passwords (not defaults)
- [ ] Network isolation (not public)
- [ ] Encryption at rest
- [ ] Encryption in transit (TLS)
- [ ] Principle of least privilege (DB users)
- [ ] Audit logging enabled
- [ ] Regular backups tested

---

## Code Security Review

### Secret Management
- [ ] No hardcoded credentials
- [ ] Secrets in environment variables or vault
- [ ] `.env` files in `.gitignore`
- [ ] No secrets in logs
- [ ] Key rotation process documented

### Dependency Security
- [ ] Dependencies up-to-date
- [ ] `npm audit` / `pip audit` clean
- [ ] Supply chain verification (checksums, signatures)
- [ ] Minimal dependencies (remove unused)
- [ ] Pin versions (no `*` or `latest`)

### Logging & Monitoring
- [ ] No sensitive data in logs
- [ ] Security events logged (auth failures, access denied)
- [ ] Log retention configured
- [ ] Alerting on suspicious activity
- [ ] Log access restricted

---

## API Security Checklist

### Authentication
- [ ] API keys or tokens required
- [ ] OAuth2/OIDC for user delegation
- [ ] Rate limiting per client
- [ ] Key rotation supported

### Authorization
- [ ] Scope-based permissions
- [ ] Resource ownership validated
- [ ] Admin endpoints protected

### Data Protection
- [ ] Input validation on all endpoints
- [ ] Output encoding (prevent XSS)
- [ ] Sensitive data encrypted in transit
- [ ] Sensitive data encrypted at rest (if stored)
- [ ] PII handling compliant (GDPR, CCPA)

### Error Handling
- [ ] No stack traces in production errors
- [ ] Generic error messages (no info leakage)
- [ ] Proper HTTP status codes
- [ ] Rate limit headers (429 Retry-After)

---

## Penetration Testing Guide

### Reconnaissance
```bash
# Port scanning (only on systems you own/have permission for)
nmap -sV -sC target.com

# Directory enumeration
gobuster dir -u https://target.com -w /usr/share/wordlists/dirb/common.txt

# Subdomain enumeration
subfinder -d target.com
```

### Common Tests
1. **SQL Injection**: `' OR '1'='1` in form fields
2. **XSS**: `<script>alert(1)</script>` in inputs
3. **Path Traversal**: `../../../etc/passwd` in file params
4. **Command Injection**: `; cat /etc/passwd` in command fields
5. **SSRF**: Internal URLs in webhook/callback params

### Tools (use responsibly, only on authorized systems)
- Burp Suite (web proxy)
- OWASP ZAP (web scanner)
- sqlmap (SQL injection)
- nmap (port scanning)
- john (password cracking)

**⚠️ Legal Warning:** Only test systems you own or have explicit written permission to test. Unauthorized testing is illegal.

---

## Incident Response Checklist

### If Compromised
1. **Contain**: Isolate affected systems
2. **Assess**: Determine scope of breach
3. **Rotate**: Revoke all potentially exposed credentials
4. **Notify**: Inform affected users (if PII exposed)
5. **Patch**: Fix the vulnerability
6. **Restore**: From clean backups if needed
7. **Review**: Post-mortem and prevent recurrence

### Credential Rotation Priority
1. Database passwords
2. API keys (internal and external)
3. SSH keys
4. Service account tokens
5. User sessions (force re-auth)

---

## Security Metrics to Track

- Mean time to detect (MTTD)
- Mean time to respond (MTTR)
- Vulnerability scan frequency
- Patch deployment time
- Security training completion
- Phishing test click rates
- Access review completion

---

*Use this checklist for security audits. Adapt based on your specific stack and threat model.*
