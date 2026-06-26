---
name: schema-json-schema-keywords
description: JSON Schema subset supported in Schema Object in Swagger 2.0
---

# Schema Object — JSON Schema Subset

The [Schema Object](schema-and-definitions.md) is based on **JSON Schema Draft 4** and uses a predefined subset. Swagger adds extra fields (discriminator, readOnly, xml, externalDocs, example) on top of this subset.

## Keywords taken directly from JSON Schema

Same meaning as in JSON Schema:

- **$ref** — JSON Reference (canonical dereferencing only).
- **format** — See [Data Type Formats](core-data-types-and-formats.md); open string in Swagger.
- **title**, **description** — GFM allowed for description.
- **default** — Unlike JSON Schema, value MUST conform to the defined type for the Schema Object.
- **multipleOf**, **maximum**, **exclusiveMaximum**, **minimum**, **exclusiveMinimum**
- **maxLength**, **minLength**, **pattern**
- **maxItems**, **minItems**, **uniqueItems**
- **maxProperties**, **minProperties**
- **required** — Array of required property names.
- **enum**, **type**
- **items** — Schema for array items (definition adjusted to use Schema Object).
- **allOf** — Array of schemas; all validated, together compose one object.
- **properties** — Map of property name → Schema Object.
- **additionalProperties** — Schema or boolean; definition adjusted to use Schema Object.

## Swagger-specific Schema fields

| Field        | Type    | Description |
|-------------|---------|-------------|
| discriminator | string | Property name for polymorphism; must be in required; value = definition name. |
| readOnly    | boolean | Property only in response; default false. |
| xml         | [XML Object](advanced-extensions-and-xml.md) | XML representation (for properties). |
| externalDocs | External Documentation Object | Extra docs. |
| example     | Any     | Example instance. |
| ^x-         | Any     | Vendor extensions. |

## Key points

- Schema can describe **primitives** and **arrays** (type + format, type: array + items), not only objects.
- Use **allOf** for composition; use **discriminator** for polymorphism (with named definitions).
- **default** in Schema MUST conform to the defined type (unlike plain JSON Schema).

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
