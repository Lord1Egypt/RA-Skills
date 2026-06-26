---
name: core-items-object
description: Items Object for non-body array parameters and header arrays in Swagger 2.0
---

# Items Object

A **limited subset** of JSON Schema's items object. Used for parameter definitions that are **not** `in: "body"` (e.g. query, path, header, formData arrays) and for [Header Object](core-header-object.md) when type is array. Files and object/model refs are **not** allowed at items level.

## When it is used

- **Parameter** with `type: "array"` and `in` ≠ body: the `items` field is an Items Object.
- **Header** with `type: "array"`: the `items` field is an Items Object.

## Fixed fields

| Field             | Type    | Required | Description |
|-------------------|---------|----------|-------------|
| type              | string  | Yes      | `string`, `number`, `integer`, `boolean`, or `array`. |
| format            | string  | No       | See [Data Type Formats](core-data-types-and-formats.md). |
| items             | Items Object | Yes if type is `array` | Nested array: items of the array. |
| collectionFormat  | string  | No       | csv, ssv, tsv, pipes (default csv). For parameters, `multi` is allowed only on the Parameter, not inside Items. |
| default           | *       | No       | Must conform to type. |
| maximum, minimum  | number  | No       | JSON Schema validation. |
| exclusiveMaximum, exclusiveMinimum | boolean | No | |
| maxLength, minLength | integer | No   | |
| pattern           | string  | No       | |
| maxItems, minItems | integer | No    | |
| uniqueItems       | boolean | No       | |
| enum              | [*]     | No       | |
| multipleOf        | number  | No       | |
| ^x-               | Any     | No       | Extensions. |

## Examples

**String items, minLength 2:**
```yaml
type: array
items:
  type: string
  minLength: 2
```

**Array of integers (0–63):**
```yaml
type: array
items:
  type: integer
  minimum: 0
  maximum: 63
```

**Nested array (array of arrays of integers):**
```yaml
type: array
items:
  type: array
  items:
    type: integer
    minimum: 0
    maximum: 63
```

## Key points

- Items Object cannot contain `$ref` or describe objects/files; only primitives and arrays of primitives (recursively).
- For body parameters use [Schema Object](schema-and-definitions.md) with `type: array` and `items` (full schema, including `$ref`).

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
