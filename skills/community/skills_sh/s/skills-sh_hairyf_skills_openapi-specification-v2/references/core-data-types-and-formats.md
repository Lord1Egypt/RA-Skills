---
name: core-data-types-and-formats
description: Primitive data types, format modifiers, and validation in Swagger 2.0
---

# Data Types and Formats

Types are based on **JSON Schema Draft 4**. Swagger adds one extra primitive: `"file"` for file upload/download (Parameter and Response). Used in Parameter (non-body), Response schema, Header, and Items.

## Type + format (spec-defined)

| Common name | type     | format    | Notes |
|-------------|----------|-----------|--------|
| integer     | integer  | int32     | Signed 32-bit. |
| long        | integer  | int64     | Signed 64-bit. |
| float       | number   | float     | |
| double      | number   | double    | |
| string      | string   | —         | |
| byte        | string   | byte      | Base64. |
| binary      | string   | binary    | Octet sequence. |
| boolean     | boolean  | —         | |
| date        | string   | date      | RFC3339 full-date. |
| dateTime    | string   | date-time | RFC3339 date-time. |
| password    | string   | password  | Hint for UIs to obscure input. |
| file        | —        | —         | Parameter/Response only; not in Schema items. |

## Open format

The `format` property is an **open string**. You can use values not in the table (e.g. `email`, `uuid`, `uri`) for documentation; validators may treat them as hints only.

## Validation (non-body parameters, Schema)

When using primitive types (including in Schema and Items), you can add JSON Schema validation:

- **Numbers:** multipleOf, maximum, exclusiveMaximum, minimum, exclusiveMinimum
- **Strings:** maxLength, minLength, pattern
- **Arrays:** maxItems, minItems, uniqueItems
- **General:** enum, default

Default must conform to the defined type. For parameters, "default" has no meaning when the parameter is required.

## Key points

- Use `type: file` only for parameters (with `in: formData`) or response schema; pair file response with appropriate `produces`.
- Prefer `format` for clarity (e.g. int32 vs int64, date vs date-time) and for codegen.
- Validation fields follow JSON Schema; Swagger does not add new validation keywords.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
