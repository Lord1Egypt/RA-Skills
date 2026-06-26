# OWASP Top 10 Detailed Test Procedures

Reference: OWASP Testing Guide v4.2 (https://owasp.org/www-project-web-security-testing-guide/)

## A01: Broken Access Control

### Insecure Direct Object Reference (IDOR)

Test method: Replace resource IDs in URLs/bodies with other users' IDs.

```
GET /api/orders/1001  → Own order ✅
GET /api/orders/1002  → Other's order → should be 403
POST /api/orders/1002/cancel → should be 403
```

Locations to test:
- URL path parameters (`/users/{id}`)
- Query parameters (`?orderId=123`)
- Request body (`{"userId": 123}`)
- File references (`/files/document_123.pdf`)

### Privilege Escalation

```
# Vertical: normal user → admin
POST /api/admin/create-user (with normal user token) → should be 403

# Role parameter tampering
POST /api/register {"username":"test", "role":"admin"} → should ignore role
```

### Missing Function-Level Access Control

Test every endpoint without auth and with lower-privilege tokens:
- Admin APIs with user token
- User A APIs with User B token
- Authenticated APIs without token

## A02: Cryptographic Failures

### TLS Configuration

```bash
# Check TLS version and cipher suites
nmap --script ssl-enum-ciphers -p 443 target.com

# Check certificate
openssl s_client -connect target.com:443 -servername target.com 2>/dev/null | \
  openssl x509 -noout -dates -subject -issuer
```

Verify:
- TLS 1.2+ only (no SSLv3, TLS 1.0/1.1)
- Strong ciphers (AES-256-GCM, CHACHA20)
- Valid certificate, not self-signed in production

### Sensitive Data in Transit

Check that these are NOT in URLs (logged by proxies/servers):
- Passwords, tokens, API keys
- Personal data (SSN, credit card)

Check that responses don't leak:
- Stack traces in production
- Internal IPs or paths
- Database column names in errors

## A03: Injection

### SQL Injection Detection

Time-based blind detection:
```
# If response delays ~5s, likely vulnerable
?id=1' AND SLEEP(5)--
?id=1' AND IF(1=1,SLEEP(5),0)--
?id=1; WAITFOR DELAY '0:0:5'--
```

Error-based detection:
```
?id=1'         → SQL syntax error = vulnerable
?id=1 AND 1=1  → normal response
?id=1 AND 1=2  → different response = injectable
```

### Cross-Site Scripting (XSS) Context

| Context | Payload | Escape Method |
|---------|---------|---------------|
| HTML body | `<script>alert(1)</script>` | HTML entity encode |
| HTML attribute | `" onmouseover="alert(1)` | Attribute encode |
| JavaScript | `'; alert(1);//` | JS encode |
| URL | `javascript:alert(1)` | URL encode |
| CSS | `expression(alert(1))` | CSS encode |

## A04: Insecure Design

### Business Logic Flaws

- Negative quantity in shopping cart → negative total?
- Applying coupon code multiple times
- Race condition: two simultaneous purchases with same inventory
- Skip steps in multi-step process (go directly to step 3)
- Price manipulation in client-side calculations

### Rate Limiting

```bash
# Test rate limiting on sensitive endpoints
for i in $(seq 1 100); do
  curl -s -o /dev/null -w "%{http_code}" "$URL/api/forgot-password" \
    -d '{"email":"test@example.com"}'
  echo " (attempt $i)"
done
# Should see 429 after threshold
```

## A05: Security Misconfiguration

Checklist:
- [ ] Default credentials changed
- [ ] Directory listing disabled
- [ ] Error pages don't expose stack traces
- [ ] Unnecessary HTTP methods disabled (TRACE, OPTIONS)
- [ ] Admin interfaces not publicly accessible
- [ ] Debug mode disabled in production
- [ ] CORS not set to wildcard (*)

```bash
# Check for common misconfigurations
curl -s "$URL/robots.txt"
curl -s "$URL/.env"
curl -s "$URL/.git/config"
curl -s "$URL/server-status"
curl -s "$URL/phpinfo.php"
curl -s "$URL/actuator/health"  # Spring Boot
curl -s "$URL/debug/vars"       # Go
```
