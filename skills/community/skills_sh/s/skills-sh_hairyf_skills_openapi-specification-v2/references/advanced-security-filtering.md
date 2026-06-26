---
name: advanced-security-filtering
description: Security filtering and empty Paths/Path Item in Swagger 2.0
---

# Security Filtering

Some objects in the Swagger spec may be **empty** or **removed** for access control over the documentation itself. This is **not** part of the formal specification; it is a pattern that some libraries use to restrict what viewers see based on authentication/authorization.

## Empty Paths Object

The [Paths Object](paths-and-operations.md) may be **empty** (no path keys). This can indicate:

- The viewer reached the right place but is not allowed to see any paths.
- They still have access to the [Info Object](core-info-metadata.md), which may contain instructions (e.g. how to authenticate to see full docs).

## Empty Path Item Object

A path key may exist but the [Path Item Object](paths-and-operations.md) may be **empty** (no get, put, post, parameters, etc.). This can indicate:

- The path exists, but the viewer cannot see operations or parameters for it.
- Finer control than hiding the path entirely: the user knows the path exists but not what they can call.

## Key points

- Empty Paths or Path Item is valid per the spec (Paths can be empty; Path Item can have no method keys).
- Use this pattern only when your tooling supports it for documentation access control.
- Not enforced by the spec; it is an optional implementation pattern.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
