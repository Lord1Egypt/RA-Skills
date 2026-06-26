---
name: schema-and-definitions
description: Schema Object, Definitions, Reference, composition and polymorphism in Swagger 2.0
---

# Schema and Definitions

## Schema Object

Based on **JSON Schema Draft 4** subset. Used for body parameters, response bodies, and `definitions`. Supports: $ref, format, title, description, default, multipleOf, maximum, minimum, maxLength, minLength, pattern, maxItems, minItems, uniqueItems, maxProperties, minProperties, required, enum, type, items, allOf, properties, additionalProperties.

Swagger-specific:

| Field       | Type    | Description |
|-------------|---------|-------------|
| discriminator | string | Property name for polymorphism; must be in required; value = schema name. |
| readOnly    | boolean | Property only in response; default false. |
| xml         | XML Object | XML representation (for properties). |
| externalDocs | External Documentation Object | Extra docs. |
| example     | Any     | Example instance. |

Root schema can describe primitives and arrays, not only objects.

## Definitions Object

At root under `definitions`. Maps name → Schema Object. Used for reusable types (models). Reference with `$ref: "#/definitions/Name"`.

## Reference Object

Only field: `$ref` (string). JSON Reference with JSON Pointer; canonical dereferencing only. Can point to same file (`#/definitions/Pet`) or external file (`Pet.json`, `definitions.yaml#/Pet`).

## Composition (allOf)

Combine schemas with `allOf` (array of schema objects). All are validated; together they form one object. No implicit hierarchy.

## Polymorphism (discriminator)

- Add `discriminator` to base schema: property name that selects subtype.
- That property MUST be in `required`.
- Value of the property = schema name in `definitions` (e.g. "Cat", "Dog").
- Inline schemas (no id) cannot be used as polymorphic targets; use definitions with names.

Example: base `Pet` with `discriminator: petType` and `required: [name, petType]`; `Cat`/`Dog` use `allOf: [{$ref: "#/definitions/Pet"}, {...}]`.

## Examples

**Simple model:**
```yaml
definitions:
  Category:
    type: object
    properties:
      id: { type: integer, format: int64 }
      name: { type: string }
```

**allOf composition:**
```yaml
ExtendedErrorModel:
  allOf:
    - $ref: "#/definitions/ErrorModel"
    - type: object
      required: [rootCause]
      properties:
        rootCause: { type: string }
```

**Map/dictionary:**
```yaml
type: object
additionalProperties:
  type: string
```

## Key points

- `definitions` is the only place to give schemas names for `$ref` and polymorphism.
- For polymorphism, discriminator property must be required; values = definition names.
- Schema can describe primitives (type + format) and arrays (type: array + items).

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
