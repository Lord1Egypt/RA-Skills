---
name: core-headers-object
description: Headers Object container for response headers in Swagger 2.0
---

# Headers Object

A **container** for the headers that can be sent as part of a response. Used in the [Response Object](responses.md) in the `headers` field.

## Structure

**Patterned fields only:** Each key is the **name** of a response header. The value is a [Header Object](core-header-object.md) that describes the type and optional validation for that header.

- Header names are case-insensitive in HTTP; the spec uses them as given (tools may normalize for display).
- No fixed fields; only header name → Header Object pairs (and optionally `^x-` extensions if the spec allows on this object; in 2.0 the Response Object's headers are just name → Header Object).

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

- Headers Object appears only inside a Response Object.
- Each entry is a header name (e.g. `X-Rate-Limit-Limit`) mapped to a full [Header Object](core-header-object.md) (type, format, description, validation, etc.).

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
