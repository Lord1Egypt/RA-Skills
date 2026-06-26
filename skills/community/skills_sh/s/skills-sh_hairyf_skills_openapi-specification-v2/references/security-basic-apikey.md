---
name: security-basic-apikey
description: basic and apiKey Security Scheme in Swagger 2.0
---

# Basic and API Key Security Schemes

When [Security Scheme Object](security.md) `type` is `basic` or `apiKey`, use the fields below. For OAuth2 see [security-oauth2-flows](security-oauth2-flows.md).

## basic

HTTP Basic Authentication (RFC 2617). No extra fields beyond `type` and optional `description`, `^x-`.

```yaml
securityDefinitions:
  basicAuth:
    type: basic
    description: HTTP Basic auth
```

Clients send `Authorization: Basic <base64(username:password)>`.

## apiKey

API key passed in a header or query parameter. **Required** fields: `type`, `name`, `in`.

| Field       | Type   | Required | Description |
|------------|--------|----------|-------------|
| type       | string | Yes      | `"apiKey"`. |
| name       | string | Yes      | Name of the header or query parameter (e.g. `X-API-Key`, `api_key`). |
| in         | string | Yes      | `"query"` or `"header"`. |
| description| string | No       | Short description. |
| ^x-        | Any    | No       | Extensions. |

```yaml
securityDefinitions:
  api_key:
    type: apiKey
    name: X-API-Key
    in: header
    description: API key in header
  query_key:
    type: apiKey
    name: api_key
    in: query
```

## Security Requirement Object

When applying these schemes in root `security` or operation `security`, use **empty array** for the scheme name (no scopes):

```yaml
security:
  - api_key: []
  - basicAuth: []
```

For OAuth2 the value is a list of required scope names; for basic and apiKey it MUST be `[]`.

## Key points

- **basic:** No `name` or `in`; client sends standard Basic auth header.
- **apiKey:** Always specify `name` and `in` (header or query).
- In Security Requirement, non-OAuth2 schemes use empty array `[]`.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
