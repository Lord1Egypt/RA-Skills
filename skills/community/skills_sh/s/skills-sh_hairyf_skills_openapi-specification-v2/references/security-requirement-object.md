---
name: security-requirement-object
description: Security Requirement Object for applying security to API or operations in Swagger 2.0
---

# Security Requirement Object

Declares which **security schemes** are required to execute the API (at root) or an operation (per operation). Used in root `security` and in [Operation Object](paths-and-operations.md) `security`.

## Structure

**Patterned fields only:** Each key MUST be the name of a security scheme declared in [Security Definitions](security.md). The value depends on the scheme type:

- **OAuth2:** Array of **scope names** required for execution (e.g. `["write:pets", "read:pets"]`).
- **basic, apiKey:** MUST be an **empty array** `[]`.

## Logic

- **Root or operation `security`:** The value is an **array** of Security Requirement objects. Between array entries: **OR** (any one satisfies). Within one entry (multiple scheme names): **AND** (all required).
- **Operation** overrides root. Use `security: []` on an operation to clear root security (no auth required for that operation).

## Examples

**API-wide: API key OR OAuth2 with scopes:**
```yaml
security:
  - api_key: []
  - petstore_auth: [write:pets, read:pets]
```

**Operation requires both API key and OAuth2:**
```yaml
security:
  - api_key: []
    petstore_auth: [read:pets]
```
(One object with two keys = AND.)

**Operation clears security:**
```yaml
security: []
```

## Key points

- Scheme names must match [Security Definitions](security.md) keys.
- OAuth2 value = list of scope names; basic/apiKey value = `[]`.
- OR between array elements; AND between keys in one element.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
