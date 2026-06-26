---
name: core-mime-types
description: MIME types for consumes and produces in Swagger 2.0
---

# MIME Types

MIME type definitions for `consumes` (request body) and `produces` (response body) MUST comply with [RFC 6838](http://tools.ietf.org/html/rfc6838). They are used at the Swagger root (global), and can be overridden at the operation level.

## Where they are used

- **Root:** `consumes` — global request body MIME types; overridable per operation (empty array clears).
- **Root:** `produces` — global response body MIME types; overridable per operation (empty array clears).
- **Operation:** `consumes`, `produces` — override or clear the global list for that operation.
- **Example Object:** Keys MUST be one of the operation's `produces` values (implicit or inherited).

## Examples (from spec)

```
text/plain; charset=utf-8
application/json
application/vnd.github+json
application/vnd.github.v3+json
application/vnd.github.v3.raw+json
application/vnd.github.v3.text+json
application/vnd.github.v3.html+json
application/vnd.github.v3.full+json
application/vnd.github.v3.diff
application/vnd.github.v3.patch
```

Common patterns: `application/json`, `application/xml`, `application/x-www-form-urlencoded`, `multipart/form-data`, `text/plain`, and vendor media types (`application/vnd.*`).

## Key points

- Use `consumes`/`produces` to document what the API accepts and returns; tools use them for codegen and UI.
- For file upload, operation must list `multipart/form-data` and/or `application/x-www-form-urlencoded` in `consumes` when using `in: formData` with `type: file`.
- Response `examples` keys must match one of the operation's `produces` values.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
