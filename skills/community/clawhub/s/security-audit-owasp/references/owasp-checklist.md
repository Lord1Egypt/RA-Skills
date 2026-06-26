# OWASP Top 10:2025 Audit Checklist

Detailed checklist for auditing each OWASP Top 10 category.

## A01 — Broken Access Control
- [ ] Test for IDOR (Insecure Direct Object References)
- [ ] Verify auth on all API endpoints
- [ ] Test privilege escalation (user → admin)
- [ ] Check for directory traversal
- [ ] Verify CORS configuration
- [ ] Test for forced browsing
- [ ] Check JWT/token validation

## A02 — Cryptographic Failures
- [ ] Verify TLS version (1.2+ only)
- [ ] Check for weak cipher suites
- [ ] Verify encryption at rest for sensitive data
- [ ] Check key management practices
- [ ] Verify password hashing (bcrypt/argon2)
- [ ] Check for plaintext credential storage
- [ ] Verify HSTS headers

## A03 — Injection
- [ ] Test SQL injection on all input fields
- [ ] Test XSS (reflected, stored, DOM-based)
- [ ] Test command injection
- [ ] Test LDAP injection
- [ ] Test template injection (SSTI)
- [ ] Verify input validation/sanitization
- [ ] Check for parameterized queries

## A04 — Insecure Design
- [ ] Review threat model documentation
- [ ] Test business logic flaws
- [ ] Verify rate limiting
- [ ] Check for race conditions
- [ ] Verify multi-factor auth where needed
- [ ] Test account lockout mechanisms

## A05 — Security Misconfiguration
- [ ] Check for default credentials
- [ ] Verify unnecessary services are disabled
- [ ] Check for verbose error messages
- [ ] Verify security headers (CSP, X-Frame, etc.)
- [ ] Check for directory listing
- [ ] Verify cloud storage permissions
- [ ] Check for sample applications

## A06 — Vulnerable Components
- [ ] Run dependency audit (npm audit, pip audit)
- [ ] Check CVE databases for known issues
- [ ] Verify patch levels
- [ ] Remove unused dependencies
- [ ] Check for outdated frameworks

## A07 — Auth Failures
- [ ] Test brute force protection
- [ ] Verify session management
- [ ] Check session timeout
- [ ] Test password reset flow
- [ ] Verify credential storage
- [ ] Check for credential stuffing protection

## A08 — Data Integrity Failures
- [ ] Verify deserialization safety
- [ ] Check CI/CD pipeline security
- [ ] Verify software supply chain integrity
- [ ] Check for unsafe auto-update mechanisms
- [ ] Verify digital signatures where needed

## A09 — Logging/Monitoring Failures
- [ ] Verify audit trail exists for all actions
- [ ] Check log integrity (tamper-proof)
- [ ] Verify alerting on anomalies
- [ ] Test incident response procedures
- [ ] Verify log retention policy
- [ ] Check for sensitive data in logs

## A10 — SSRF
- [ ] Test for internal resource access via URLs
- [ ] Verify URL validation and allowlists
- [ ] Check for cloud metadata endpoint access
- [ ] Test for blind SSRF
- [ ] Verify egress filtering