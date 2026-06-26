---
name: paths-and-operations
description: Paths Object, Path Item, and Operation Object in Swagger 2.0
---

# Paths and Operations

## Paths Object

Maps relative path strings to Path Item objects. Path is appended to `basePath` to form the full URL. Path keys MUST start with `/`. Path templating is allowed (e.g. `/pets/{petId}`). Paths may be empty (e.g. for ACL filtering).

## Path Item Object

Describes operations on a single path.

| Field       | Type    | Description |
|-------------|---------|-------------|
| $ref        | string  | External Path Item (conflicts with local = undefined). |
| get, put, post, delete, options, head, patch | Operation Object | One per HTTP method. |
| parameters  | [Parameter \| $ref] | Parameters for all operations on this path. Can be overridden at operation level, not removed. No duplicate name+in. At most one body parameter. |

Path-level `parameters` apply to every operation on that path; operation-level parameters override but cannot remove them.

## Operation Object

Describes one API operation.

| Field        | Type    | Required | Description |
|--------------|---------|----------|-------------|
| tags         | [string]| No       | Tags for grouping. |
| summary      | string  | No       | Short summary; &lt; 120 chars recommended for UI. |
| description  | string  | No       | Detailed behavior; GFM allowed. |
| externalDocs | External Documentation Object | No | Extra docs. |
| operationId  | string  | No       | Unique ID for the operation; use for codegen. |
| consumes     | [string]| No       | Overrides global consumes; [] clears. |
| produces     | [string]| No       | Overrides global produces; [] clears. |
| parameters   | [Parameter \| $ref] | No | Operation parameters; overrides path params, at most one body. |
| responses    | Responses Object | Yes | Possible responses. |
| schemes      | [string]| No       | Overrides root schemes: http, https, ws, wss. |
| deprecated   | boolean | No       | Default false. |
| security     | [Security Requirement Object] | No | Overrides root security; [] removes. |
| ^x-          | Any     | No       | Extensions. |

## Example

```yaml
paths:
  /pets:
    get:
      summary: List pets
      operationId: listPets
      produces: [application/json]
      responses:
        "200":
          description: A list of pets.
          schema:
            type: array
            items:
              $ref: "#/definitions/Pet"
    parameters:
      - name: id
        in: path
        required: true
        type: array
        items:
          type: string
        collectionFormat: csv
```

## Key points

- Operation **must** have `responses` with at least one code; should document success (e.g. 200).
- Uniqueness of parameters: `name` + `in` (e.g. one `query` param named `id`).
- Use `operationId` for stable client/server code generation.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
