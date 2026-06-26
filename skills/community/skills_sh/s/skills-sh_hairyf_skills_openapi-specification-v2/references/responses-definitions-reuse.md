---
name: responses-definitions-reuse
description: Root-level Responses Definitions Object and reusing responses via $ref in Swagger 2.0
---

# Responses Definitions (Reuse)

The root **responses** object holds reusable response definitions. It does **not** define global responses for all operations; each operation must declare its own `responses` and can reference these via `$ref`.

## Location

At root of the Swagger Object:

```yaml
swagger: "2.0"
info: { ... }
paths: { ... }
responses:
  NotFound: { ... }
  GeneralError: { ... }
```

## Structure

Patterned object: each key is a logical name, value is a full [Response Object](responses.md). Reference in operation responses with `$ref: "#/responses/name"`.

## Example

```yaml
responses:
  NotFound:
    description: Entity not found.
  IllegalInput:
    description: Illegal input for operation.
  GeneralError:
    description: General Error
    schema:
      $ref: "#/definitions/GeneralError"
  NoContent:
    description: Operation succeeded, no body returned.
```

## Using in operations

```yaml
paths:
  /pets/{id}:
    get:
      responses:
        "200":
          description: The pet
          schema:
            $ref: "#/definitions/Pet"
        "404":
          $ref: "#/responses/NotFound"
        "default":
          $ref: "#/responses/GeneralError"
```

You can mix inline responses and references in the same operation.

## Key points

- Root `responses` is a **library** only; no response is applied to every operation.
- Use for common error or success shapes (404, 400, 500, 204) so operations stay consistent and short.
- Operation `responses` must contain at least one entry; use `default` with a reference to cover unspecified status codes.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
