---
name: security-tester
description: >
  Security testing for web applications and APIs based on OWASP standards.
  Identify common vulnerabilities (injection, auth bypass, XSS, CSRF, IDOR),
  generate security test cases, analyze scan results, and write security test reports.
  Follows OWASP Testing Guide v4.2, OWASP Top 10 (2021), and CWE classifications.
  Use when: (1) security testing web apps or APIs, (2) writing security test cases,
  (3) analyzing vulnerability scan results, (4) OWASP Top 10 verification,
  (5) authentication/authorization testing, (6) input validation testing,
  (7) "安全测试", "漏洞测试", "OWASP", "XSS测试", "SQL注入", "渗透测试",
  "权限测试", "越权测试", "IDOR", "CSRF".
  NOT for: code-level static analysis (use SAST tools), infrastructure penetration
  testing (use dedicated pentest tools), or compliance auditing (use GRC tools).
---

# Security Tester

Test web application and API security based on OWASP standards.

## OWASP Top 10 (2021) Test Matrix

Reference: https://owasp.org/Top10/

| # | Category | CWE | Key Tests |
|---|----------|-----|-----------|
| A01 | Broken Access Control | CWE-284 | IDOR, privilege escalation, force browse, CORS |
| A02 | Cryptographic Failures | CWE-310 | TLS config, password storage, sensitive data exposure |
| A03 | Injection | CWE-74 | SQLi, XSS, command injection, LDAP injection |
| A04 | Insecure Design | CWE-501 | Business logic flaws, missing rate limits |
| A05 | Security Misconfiguration | CWE-16 | Default creds, verbose errors, unnecessary features |
| A06 | Vulnerable Components | CWE-1035 | Outdated libs, known CVEs |
| A07 | Auth Failures | CWE-287 | Brute force, weak passwords, session fixation |
| A08 | Data Integrity Failures | CWE-502 | Insecure deserialization, unsigned updates |
| A09 | Logging Failures | CWE-778 | Missing audit logs, log injection |
| A10 | SSRF | CWE-918 | Server-side request forgery |

## Security Test Case Generation

For each API endpoint or page, apply this checklist:

### A01: Access Control Testing (OWASP-AT)

```bash
# IDOR: Access another user's resource
curl -H "Authorization: Bearer $USER_A_TOKEN" \
  "$URL/api/users/USER_B_ID/profile"
# Expected: 403 Forbidden

# Horizontal privilege escalation
curl -H "Authorization: Bearer $NORMAL_USER_TOKEN" \
  "$URL/api/admin/users"
# Expected: 403 Forbidden

# Force browsing (unauthenticated)
curl "$URL/api/internal/config"
# Expected: 401 Unauthorized

# CORS misconfiguration
curl -H "Origin: https://evil.com" -I "$URL/api/data"
# Check: Access-Control-Allow-Origin should NOT be * or evil.com

# HTTP method tampering
curl -X DELETE -H "Authorization: Bearer $READONLY_TOKEN" \
  "$URL/api/items/1"
# Expected: 403 if user lacks delete permission
```

### A03: Injection Testing

```bash
# SQL Injection (OWASP-DV-005)
# Reference: CWE-89
PAYLOADS=(
  "' OR '1'='1"
  "' OR '1'='1' --"
  "'; DROP TABLE users; --"
  "' UNION SELECT null,null,null --"
  "1' AND SLEEP(5) --"
)
for p in "${PAYLOADS[@]}"; do
  echo "Testing: $p"
  curl -s -o /dev/null -w "%{http_code} %{time_total}s" \
    "$URL/api/search?q=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$p'))")"
  echo
done

# XSS (OWASP-DV-001)
# Reference: CWE-79
XSS_PAYLOADS=(
  '<script>alert(1)</script>'
  '<img src=x onerror=alert(1)>'
  '"><svg onload=alert(1)>'
  "javascript:alert(1)"
  '<body onload=alert(1)>'
)

# Command Injection (CWE-78)
CMD_PAYLOADS=(
  '; ls -la'
  '| cat /etc/passwd'
  '$(whoami)'
  '`id`'
)
```

### A07: Authentication Testing

```bash
# Brute force protection (OWASP-AT-004)
for i in $(seq 1 20); do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST "$URL/api/login" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"admin\",\"password\":\"wrong$i\"}")
  echo "Attempt $i: $STATUS"
  # After 5-10 attempts, should see 429 or account lockout
done

# Session fixation
# 1. Get session before login
# 2. Login
# 3. Verify session ID changed after login

# JWT vulnerabilities
# Check: alg=none bypass, weak secret, missing expiry
echo "$JWT" | cut -d. -f2 | base64 -d 2>/dev/null | python3 -m json.tool
```

## Vulnerability Report Template

```markdown
## 🛡️ Security Finding

**Title**: [CWE-XXX] Brief description
**Severity**: 🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low / ℹ️ Info
**CVSS 3.1**: X.X ({vector_string})
**CWE**: CWE-XXX ({cwe_name})
**OWASP**: A0X:2021 ({category})
**Affected**: {endpoint / component}

### Description
What the vulnerability is and why it matters.

### Proof of Concept
Step-by-step reproduction with exact commands/requests.

### Impact
- Confidentiality: {High/Medium/Low/None}
- Integrity: {High/Medium/Low/None}
- Availability: {High/Medium/Low/None}

### Remediation
Specific fix recommendations with code examples.

### References
- OWASP: {link}
- CWE: {link}
```

### CVSS 3.1 Quick Scoring (Reference: https://www.first.org/cvss/)

| Severity | Score | Example |
|----------|-------|---------|
| 🔴 Critical | 9.0-10.0 | Unauthenticated RCE, mass data breach |
| 🟠 High | 7.0-8.9 | SQLi with data access, auth bypass |
| 🟡 Medium | 4.0-6.9 | Stored XSS, IDOR with limited data |
| 🟢 Low | 0.1-3.9 | Reflected XSS requiring interaction |
| ℹ️ Info | 0.0 | Version disclosure, missing headers |

## Security Headers Check

```bash
# Check response headers
curl -sI "$URL" | grep -iE "strict-transport|content-security|x-frame|x-content-type|x-xss|referrer-policy|permissions-policy"

# Expected headers:
# Strict-Transport-Security: max-age=31536000; includeSubDomains
# Content-Security-Policy: default-src 'self'
# X-Frame-Options: DENY or SAMEORIGIN
# X-Content-Type-Options: nosniff
# Referrer-Policy: strict-origin-when-cross-origin
# Permissions-Policy: camera=(), microphone=()
```

## References

For detailed testing procedures per category:
- **OWASP Top 10 detailed tests**: See `references/owasp-top10-tests.md`
- **API-specific security**: See `references/api-security.md`
