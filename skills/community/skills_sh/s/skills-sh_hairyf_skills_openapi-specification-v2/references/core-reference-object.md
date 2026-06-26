---
name: core-reference-object
description: Reference Object ($ref), JSON Pointer, and multi-file references in Swagger 2.0
---

# Reference Object

Allows referencing other definitions in the spec. Used for reusable parameters, responses, and schemas. Swagger 2.0 supports **canonical dereferencing** only (JSON Reference with JSON Pointer).

## Structure

Single field:

| Field | Type   | Required | Description |
|-------|--------|----------|-------------|
| $ref  | string | Yes      | The reference string (JSON Pointer or file path). |

## Same-document references

Use JSON Pointer relative to document root. Common patterns:

- **Definition:** `#/definitions/ModelName`
- **Parameter:** `#/parameters/paramName`
- **Response:** `#/responses/responseName`

```yaml
schema:
  $ref: "#/definitions/Pet"
```

```yaml
parameters:
  - $ref: "#/parameters/skipParam"
  - $ref: "#/parameters/limitParam"
```

## External file references

**Schema in another file:**
```yaml
$ref: "Pet.json"
$ref: "definitions.yaml#/Pet"
```

**Relative path + fragment:**
```yaml
$ref: "definitions.json#/Pet"
```

Path is relative to the current document. Fragment (`#/...`) is a JSON Pointer into that document.

## Where $ref is used

- **Path Item:** `$ref` to external Path Item (entire path). Conflicts with local path fields = undefined.
- **Parameter:** Reference root `parameters` entry.
- **Response:** Reference root `responses` entry.
- **Schema:** Reference `definitions` or external file; in Schema Object for body/response, and in `allOf` for composition.

## Key points

- Only canonical dereferencing: resolve `$ref` to the target and replace; no merging of sibling fields with the reference.
- Parameter/response reuse: define once under root `parameters` / `responses`, reference by `#/parameters/name` or `#/responses/name`.
- Definition names are the keys under `definitions`; use those in `#/definitions/Name` and in discriminator values for polymorphism.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
