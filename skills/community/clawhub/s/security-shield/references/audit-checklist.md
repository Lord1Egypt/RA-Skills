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
grep -r "<secret_prefix>" --include="*.py" --include="*.js" .  # pattern only - never test against real systems

# 4. Verify .gitignore excludes secrets
cat .gitignore | grep -E "\.env|secrets|keys"
```

---

## Download Verification Checklist

Use before trusting or executing anything obtained from outside the system.

- [ ] Source confirmed (official site/registry, verified publisher)
- [ ] Checksum/hash matches a trusted published reference
- [ ] Signature verified (sigstore/cosign, GPG, or platform signature)
- [ ] Provenance recorded (who built it, when, from what)
- [ ] Scanned with available tools (Trivy, VirusTotal, OSV-Scanner)
- [ ] Contents inspected (scripts, archives, embedded commands)
- [ ] Executed in a sandbox/container before normal use
- [ ] Outcome documented in the security log

**Rule:** missing evidence on any check = content remains untrusted.

---

## Agent & AI Security Checklist

- [ ] Tool/skill source and publisher verified before install
- [ ] Skills audited for concealed instructions or hidden commands
- [ ] Agent runs in a sandboxed / containerized environment
- [ ] External content treated as data, never as directives
- [ ] No real credentials placed in prompts or model context
- [ ] High-risk tool actions require human approval
- [ ] Agent memory cleared between unrelated tasks
- [ ] Prompt-and-response logs reviewed for data leakage

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
- [ ] SBOM generated (SPDX / CycloneDX) for releases
- [ ] SLSA provenance recorded and hosted
- [ ] Images and binaries signed (sigstore / cosign)

### Modern Scanning Tools
- [ ] Container scan with Trivy / Grype on every image
- [ ] OSV-Scanner for open-source vulnerability lookups
- [ ] Secrets scanning with gitleaks / TruffleHog in CI
- [ ] IaC scan with checkov / tfsec / KICS
- [ ] License + dependency policy enforcement

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

- Access review completion

---

*Use this checklist for security audits. Adapt based on your specific stack and threat model.*
