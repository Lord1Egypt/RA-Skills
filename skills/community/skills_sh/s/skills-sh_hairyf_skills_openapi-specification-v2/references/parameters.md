---
name: parameters
description: Parameter Object, locations, body vs non-body, and Items Object in Swagger 2.0
---

# Parameters

A parameter is uniquely identified by **name** + **in** (location). At most **one body** parameter per operation.

## Parameter locations (`in`)

| in         | Description |
|------------|-------------|
| path       | Part of URL path; use with path templating. **required** MUST be true. |
| query      | Appended to URL. |
| header     | Request header. |
| body       | Request body; one only. Name is for docs only. Incompatible with formData. |
| formData   | For `application/x-www-form-urlencoded` or `multipart/form-data`. Use for file uploads (`type: file`). Incompatible with body. |

## When `in` is `"body"`

- **Required:** `schema` (Schema Object). No `type`/`format`/`items` etc. at parameter level.
- Describes the whole body (object, array, or primitive via schema).

## When `in` is not `"body"`

- **Required:** `type` — one of `string`, `number`, `integer`, `boolean`, `array`, `file`.
- Optional: `format`, `allowEmptyValue` (query/formData), `items` (if type array), `collectionFormat`, `default`, and JSON Schema validation (maximum, minimum, maxLength, pattern, enum, etc.).

## collectionFormat (non-body arrays)

- `csv` (default) — `foo,bar`
- `ssv` — `foo bar`
- `tsv` — `foo\tbar`
- `pipes` — `foo|bar`
- `multi` — multiple params `foo=bar&foo=baz` (query or formData only)

## Examples

**Body (reference):**
```yaml
name: user
in: body
required: true
schema:
  $ref: "#/definitions/User"
```

**Path:**
```yaml
name: petId
in: path
required: true
type: string
description: ID of pet
```

**Query array (multi):**
```yaml
name: id
in: query
required: false
type: array
items:
  type: string
collectionFormat: multi
```

**Form file:**
```yaml
name: avatar
in: formData
required: true
type: file
```
Consumes must be `multipart/form-data` and/or `application/x-www-form-urlencoded`.

## Items Object

Used for non-body **array** parameters (and headers). Same idea as Schema but limited: `type` (string, number, integer, boolean, array), `format`, `items`, `collectionFormat`, `default`, and JSON Schema validation fields. No `file` or object ref at items level.

## Key points

- Path parameters: `name` MUST match the path segment (e.g. path `/pets/{petId}` → name `petId`).
- Body and formData cannot both be used on the same operation.
- Reuse parameters via root `parameters` and `$ref` (e.g. `$ref: "#/parameters/skipParam"`).

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
