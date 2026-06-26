---
name: core-fixed-patterned-fields
description: Fixed fields vs patterned fields in Swagger 2.0
---

# Fixed and Patterned Fields

The Swagger schema exposes two kinds of fields. This affects how you add or extend content.

## Fixed fields

- **Declared name:** Exactly one occurrence per object (e.g. `swagger`, `info`, `paths`, `title`, `version`).
- **Type and meaning** are defined by the spec.
- Example: Swagger Object has fixed field `swagger` (string), `info` (Info Object), `paths` (Paths Object), etc.

## Patterned fields

- **Regex pattern** for the field name (e.g. `/{path}` for Paths, `^x-` for extensions).
- **Multiple occurrences** allowed as long as each name is unique (e.g. multiple paths, multiple `x-` keys).
- Examples:
  - **Paths Object:** Pattern `/{path}` — each key is a path string starting with `/`.
  - **Definitions Object:** Pattern `{name}` — each key is a definition name.
  - **Extensions:** Pattern `^x-` — any key starting with `x-`.

## Where each appears

- **Swagger Object:** Fixed (swagger, info, host, basePath, paths, …), Patterned (^x-).
- **Paths Object:** Patterned (/{path}, ^x-).
- **Path Item:** Fixed ($ref, get, put, post, parameters, …), Patterned (^x-).
- **Responses Object:** Fixed (default), Patterned (HTTP status code keys, ^x-).
- **Definitions, parameters, responses, securityDefinitions:** Patterned only (name → value).
- **Example Object, Headers Object, Scopes Object:** Patterned only (e.g. MIME type → value, header name → Header Object).

## Key points

- Use fixed fields for standard structure; use patterned fields for open-ended maps (paths, definitions, headers, examples, x-).
- Patterned field names must be unique within that object (e.g. no duplicate path keys, no duplicate definition names).

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
