---
name: security-oauth2-flows
description: OAuth2 security scheme flows and required URLs in Swagger 2.0
---

# OAuth2 Flows (Security Scheme)

When `type` is `oauth2`, the Security Scheme Object must include `flow` and the URLs required for that flow. Scopes are required for all OAuth2 schemes.

## Flows and required fields

| flow         | authorizationUrl | tokenUrl | Use case |
|--------------|------------------|----------|----------|
| implicit     | Required         | No       | Client-side; token in redirect. |
| password     | No               | Required | Resource owner password. |
| application  | No               | Required | Client credentials. |
| accessCode   | Required         | Required | Authorization code. |

## Examples

**Implicit (e.g. browser redirect):**
```yaml
petstore_auth:
  type: oauth2
  authorizationUrl: http://swagger.io/api/oauth/dialog
  flow: implicit
  scopes:
    write:pets: modify pets in your account
    read:pets: read your pets
```

**Password (resource owner):**
```yaml
oauth2Password:
  type: oauth2
  tokenUrl: https://api.example.com/oauth/token
  flow: password
  scopes:
    read: read access
```

**Application (client credentials):**
```yaml
oauth2Application:
  type: oauth2
  tokenUrl: https://api.example.com/oauth/token
  flow: application
  scopes:
    admin: full access
```

**Access code (authorization code):**
```yaml
oauth2AccessCode:
  type: oauth2
  authorizationUrl: https://api.example.com/oauth/authorize
  tokenUrl: https://api.example.com/oauth/token
  flow: accessCode
  scopes:
    read: read access
```

## Scopes Object

Always required for oauth2. Maps scope name → short description. In [Security Requirement Object](security.md), the value for an oauth2 scheme is the list of required scope names; for non-oauth2 schemes use empty array `[]`.

## Key points

- Use `implicit` or `accessCode` when the client gets an authorization code or token via browser redirect; provide `authorizationUrl` (and for accessCode, `tokenUrl`).
- Use `password` or `application` for server-to-server or trusted clients; only `tokenUrl` is required.
- Names in the spec are `implicit`, `password`, `application`, `accessCode` (not "client_credentials" or "authorization_code").

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
