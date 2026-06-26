---
name: core-path-templating
description: Path templating and path parameters in Swagger 2.0
---

# Path Templating

Path templating uses **curly braces `{}`** to mark a section of the URL path as replaceable by a [path parameter](parameters.md). The path is appended to [`basePath`](core-swagger-object.md) to form the full URL.

## Rules

- **Path keys** in the [Paths Object](paths-and-operations.md) MAY contain templated segments, e.g. `/pets/{petId}`, `/users/{userId}/orders`.
- **Path parameters:** Each templated segment MUST have a corresponding parameter with `in: "path"` and `name` matching the segment name (e.g. path `/pets/{petId}` → parameter `name: petId`, `in: path`).
- **Required:** Path parameters MUST have `required: true`.
- **No templating** in `host` or `basePath`; they do not support path templating.

## Parameter name and path segment

The parameter `name` MUST correspond to the path segment:

- Path: `/items/{itemId}` → use a parameter with `name: "itemId"`, `in: "path"`.
- Path: `/pets/{petId}/photos/{photoId}` → two path parameters: `petId` and `photoId`.

## Example

```yaml
paths:
  /pets/{petId}:
    get:
      parameters:
        - name: petId
          in: path
          required: true
          type: string
          description: ID of the pet
      responses:
        "200":
          description: The pet
          schema:
            $ref: "#/definitions/Pet"
```

## Key points

- Path parameter names are **case sensitive** and must match the segment inside `{}` exactly.
- Each path segment in `{}` must be covered by exactly one path parameter with matching `name`.
- Path-level `parameters` can include the path parameter(s) so all operations on that path inherit them.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
