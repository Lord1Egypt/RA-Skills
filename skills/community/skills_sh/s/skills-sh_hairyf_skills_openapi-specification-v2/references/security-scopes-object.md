---
name: security-scopes-object
description: Scopes Object for OAuth2 security scheme in Swagger 2.0
---

# Scopes Object

Lists the **available scopes** for an OAuth2 [Security Scheme](security.md). Used only when `type` is `oauth2`; the Security Scheme Object **requires** a `scopes` field of type Scopes Object.

## Structure

**Patterned fields only:** Each key is a **scope name**. The value is a **string** — a short description of that scope.

- **Patterned:** `{name}` → string (scope name → description).
- **Extensions:** Pattern `^x-` allowed (any value).

## Example

```yaml
scopes:
  write:pets: modify pets in your account
  read:pets: read your pets
  admin: full administrative access
```

In a Security Scheme:

```yaml
securityDefinitions:
  petstore_auth:
    type: oauth2
    authorizationUrl: http://swagger.io/api/oauth/dialog
    flow: implicit
    scopes:
      write:pets: modify pets in your account
      read:pets: read your pets
```

## Use in Security Requirement

In a [Security Requirement Object](security.md), for an OAuth2 scheme the value is a **list of scope names** required for that operation. For non-OAuth2 schemes the value MUST be an empty array `[]`.

```yaml
security:
  - petstore_auth: [write:pets, read:pets]
```

## Key points

- Scopes Object is required for every OAuth2 Security Scheme.
- Keys are scope names; values are human-readable descriptions.
- Security Requirement lists which scopes are required (OAuth2) or use `[]` (basic, apiKey).

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
