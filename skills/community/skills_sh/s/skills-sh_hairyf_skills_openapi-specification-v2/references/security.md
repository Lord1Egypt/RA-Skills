---
name: security
description: Security Definitions, Security Scheme, Security Requirement, and Scopes in Swagger 2.0
---

# Security

## Security Definitions Object

At root: `securityDefinitions`. Maps scheme name → Security Scheme Object. Declares available schemes; does not enforce them.

## Security Scheme Object

| Field            | Type   | When       | Description |
|------------------|--------|------------|-------------|
| type             | string | Required   | `basic`, `apiKey`, or `oauth2`. |
| description      | string | No         | Short description. |
| name             | string | apiKey     | Header or query parameter name. |
| in               | string | apiKey     | `query` or `header`. |
| flow             | string | oauth2     | `implicit`, `password`, `application`, or `accessCode`. |
| authorizationUrl | string | oauth2 (implicit, accessCode) | Required. |
| tokenUrl         | string | oauth2 (password, application, accessCode) | Required. |
| scopes           | Scopes Object | oauth2 | Required. |

**basic:** no extra fields.  
**apiKey:** name + in.  
**oauth2:** flow + authorizationUrl/tokenUrl (per flow) + scopes.

## Scopes Object

Maps scope name → short description (e.g. `write:pets: "modify pets"`).

## Security Requirement Object

Applied at root (`security`) or per operation (`security`). List is OR: any one entry can satisfy. Each entry is an object: scheme name → array. For oauth2 the array is required scope names; for basic/apiKey use empty array `[]`.

```yaml
security:
  - api_key: []
  - petstore_auth: [write:pets, read:pets]
```

Operation overrides root; use `security: []` to clear.

## Examples

**API Key (header):**
```yaml
securityDefinitions:
  api_key:
    type: apiKey
    name: api_key
    in: header
```

**Basic:**
```yaml
securityDefinitions:
  basicAuth:
    type: basic
```

**OAuth2 implicit:**
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

## Key points

- Root `security` = default for all operations; operations can override or disable.
- Multiple entries in `security` = OR; within one entry (multiple schemes) = AND (all required).
- OAuth2 flow dictates which of authorizationUrl/tokenUrl are required.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
