---
name: core-http-status-codes
description: HTTP status codes as response keys and default response in Swagger 2.0
---

# HTTP Status Codes

Response keys in the [Responses Object](responses.md) are HTTP status codes. The available codes are described by [RFC 7231](http://tools.ietf.org/html/rfc7231#section-6) and the [IANA HTTP Status Code Registry](http://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml).

## Usage in Responses Object

- **Keys:** Any valid HTTP status code (e.g. `"200"`, `"201"`, `"400"`, `"404"`, `"500"`). One property per status code.
- **default:** Special key for responses not declared for a specific code. Use for generic error or fallback documentation.
- **At least one** response code MUST be present per operation. The spec recommends documenting a **success** response (e.g. 200 or 201).

## Example

```yaml
responses:
  "200":
    description: Success
    schema:
      $ref: "#/definitions/Pet"
  "400":
    description: Bad request
    schema:
      $ref: "#/definitions/Error"
  "404":
    $ref: "#/responses/NotFound"
  default:
    description: Unexpected error
    schema:
      $ref: "#/definitions/Error"
```

In YAML, numeric keys like `200` are often quoted (`'200'`) to avoid type coercion.

## Key points

- Use `default` to cover unspecified status codes (e.g. 5xx or unknown errors).
- Document at least one success response; tools and clients rely on it.
- Status codes are strings in the spec (e.g. `"200"` in JSON, `'200'` in YAML).

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
