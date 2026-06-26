# Backend Security

OWASP Top 10, security best practices, and input validation.

## OWASP Top 10 (2025)

1. **Broken Access Control** - Implement proper authorization checks
2. **Cryptographic Failures** - Use strong encryption, secure storage
3. **Injection** - Parameterized queries, input validation
4. **Insecure Design** - Security by design, threat modeling
5. **Security Misconfiguration** - Secure defaults, regular updates
6. **Vulnerable Components** - Dependency scanning, updates
7. **Authentication Failures** - Strong passwords, MFA, session management
8. **Software and Data Integrity** - Code signing, supply chain security
9. **Security Logging Failures** - Comprehensive logging, monitoring
10. **Server-Side Request Forgery** - Input validation, allowlists

## Input Validation

### Principles
- Validate all inputs at API boundaries
- Whitelist over blacklist
- Validate type, format, length, range
- Sanitize before processing

### Examples

**Type Validation:**
```python
def validate_user_id(user_id: str) -> int:
    try:
        return int(user_id)
    except ValueError:
        raise ValidationError("Invalid user ID")
```

**Format Validation:**
```python
import re

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

## SQL Injection Prevention

**Always use parameterized queries:**

```python
# BAD - Vulnerable
query = f"SELECT * FROM users WHERE id = {user_id}"

# GOOD - Safe
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

## Password Security

- Use Argon2id for password hashing
- Minimum 12 characters, complexity requirements
- Never store plaintext passwords
- Implement password reset securely
- Rate limit login attempts

## Authentication

- OAuth 2.1 + PKCE for authorization
- JWT tokens with short expiration
- Refresh tokens for long sessions
- Secure token storage
- CSRF protection

## Security Headers

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
Content-Security-Policy: default-src 'self'
```

## Rate Limiting

- Implement rate limits to prevent abuse
- Different limits for authenticated vs anonymous
- Return 429 Too Many Requests when exceeded
- Log rate limit violations

## Secrets Management

- Never commit secrets to version control
- Use environment variables or secret managers
- Rotate secrets regularly
- Use different secrets for different environments

## Dependency Security

- Regularly update dependencies
- Use dependency scanning tools
- Review security advisories
- Pin dependency versions
- Use lock files
