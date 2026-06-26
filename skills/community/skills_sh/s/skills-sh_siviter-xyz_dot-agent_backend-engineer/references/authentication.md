# Authentication & Authorization

OAuth 2.1, JWT, RBAC, MFA, and session management.

## OAuth 2.1

### Flow
1. Client redirects to authorization server
2. User authenticates and authorizes
3. Authorization server returns authorization code
4. Client exchanges code for access token
5. Client uses access token for API requests

### PKCE (Proof Key for Code Exchange)
- Required for public clients
- Prevents authorization code interception
- Generate code verifier and challenge

### Best Practices
- Use HTTPS only
- Short-lived access tokens (15 minutes)
- Long-lived refresh tokens (7-30 days)
- Secure token storage
- Token revocation support

## JWT (JSON Web Tokens)

### Structure
```
header.payload.signature
```

### Claims
- `iss` (issuer)
- `sub` (subject)
- `exp` (expiration)
- `iat` (issued at)
- Custom claims for user data

### Best Practices
- Sign with strong algorithm (RS256, ES256)
- Short expiration times
- Include minimal user data
- Validate signature and expiration
- Use refresh tokens for long sessions

## Role-Based Access Control (RBAC)

### Roles
- Admin - Full access
- User - Standard access
- Guest - Limited access

### Permissions
- Read, Write, Delete
- Resource-specific permissions
- Hierarchical roles

### Implementation
```python
def require_permission(permission: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not current_user.has_permission(permission):
                raise ForbiddenError()
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## Multi-Factor Authentication (MFA)

### Methods
- TOTP (Time-based One-Time Password)
- SMS codes
- Email codes
- Hardware tokens
- Biometric authentication

### Implementation
- Require MFA for sensitive operations
- Backup codes for account recovery
- Rate limit MFA attempts
- Secure MFA storage

## Session Management

### Best Practices
- Use secure, HTTP-only cookies
- Set SameSite attribute
- Implement session timeout
- Regenerate session ID on login
- Secure session storage
- Invalidate on logout

### Session Storage
- Server-side sessions (Redis, database)
- Stateless sessions (JWT)
- Hybrid approach

## Password Reset

### Secure Flow
1. User requests password reset
2. Generate secure, time-limited token
3. Send reset link via email
4. Validate token on reset page
5. Require new password + confirmation
6. Invalidate token after use

### Security Considerations
- Rate limit reset requests
- Token expiration (1 hour)
- One-time use tokens
- Secure token generation
- Email verification
