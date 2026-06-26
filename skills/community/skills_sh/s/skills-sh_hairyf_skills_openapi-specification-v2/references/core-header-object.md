---
name: core-header-object
description: Header Object for response headers in Swagger 2.0
---

# Header Object

Describes a single response header. Used inside the [Headers Object](responses.md) (response `headers`). Same type system as non-body parameters: simple types only (no body/model ref at header level).

## Fixed fields

| Field             | Type    | Required | Description |
|-------------------|---------|----------|-------------|
| description       | string  | No       | Short description; GFM allowed. |
| type              | string  | Yes      | One of `string`, `number`, `integer`, `boolean`, `array`. |
| format            | string  | No       | Same as [Data Type Formats](core-data-types-and-formats.md). |
| items             | Items Object | Yes if type is `array` | Item type for array headers. |
| collectionFormat  | string  | No       | csv, ssv, tsv, pipes (default csv). No `multi` for headers. |
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

## Example

```yaml
headers:
  X-Rate-Limit-Limit:
    description: The number of allowed requests in the current period
    type: integer
  X-Rate-Limit-Remaining:
    description: The number of remaining requests in the current period
    type: integer
  X-Rate-Limit-Reset:
    description: The number of seconds left in the current period
    type: integer
  X-Request-Id:
    description: Request correlation ID
    type: string
    format: uuid
```

## Key points

- Header names are case-insensitive in HTTP but are given as-is in the spec; tools may normalize for display.
- Use `type: array` and `items` for headers that send multiple values (e.g. `Accept-Encoding`); use `collectionFormat` to document serialization (csv, ssv, tsv, pipes).

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
