---
name: responses
description: Responses Object, Response Object, Headers, and Example in Swagger 2.0
---

# Responses

## Responses Object (operation level)

Maps HTTP status codes (and `default`) to response definitions. **Must** contain at least one response. Should document success (e.g. 200). Keys are status codes or `default`; values are Response Object or `$ref` to root `responses`.

```yaml
responses:
  "200":
    description: a pet to be returned
    schema:
      $ref: "#/definitions/Pet"
  "404":
    $ref: "#/responses/NotFound"
  default:
    description: Unexpected error
    schema:
      $ref: "#/definitions/ErrorModel"
```

## Response Object

| Field        | Type   | Required | Description |
|--------------|--------|----------|-------------|
| description  | string | Yes      | Short description; GFM allowed. |
| schema       | Schema Object | No | Response body (primitive, array, object). Root type may be `"file"`; pair with produces. |
| headers      | Headers Object | No | Response headers. |
| examples     | Example Object | No | Example per MIME type. |
| ^x-          | Any    | No       | Extensions. |

No schema = no response body.

## Headers Object

Maps header name to Header Object (description, type, format, items, collectionFormat, default, and JSON Schema validation). Type required; one of string, number, integer, boolean, array.

## Example Object

Maps MIME type (should be in operation `produces`) to example value:

```yaml
examples:
  application/json:
    name: Puma
    type: Dog
```

## Reuse

Define under root `responses` and reference:

```yaml
# root
responses:
  NotFound:
    description: Entity not found.
  GeneralError:
    description: General Error
    schema:
      $ref: "#/definitions/GeneralError"

# in operation
responses:
  "404":
    $ref: "#/responses/NotFound"
```

## Key points

- Every operation must have at least one response; document success and important errors.
- Use `default` for unspecified status codes.
- Response `schema` can be primitive/array/object; use `$ref` for definitions.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
