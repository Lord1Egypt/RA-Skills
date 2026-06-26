---
name: parameters-definitions-reuse
description: Root-level Parameters Definitions Object and reusing parameters via $ref in Swagger 2.0
---

# Parameters Definitions (Reuse)

The root **parameters** object holds reusable parameter definitions. It does **not** define global parameters for all operations; each operation or path must reference parameters explicitly via `$ref`.

## Location

At root of the Swagger Object:

```yaml
swagger: "2.0"
info: { ... }
paths: { ... }
parameters:
  skipParam: { ... }
  limitParam: { ... }
```

## Structure

Patterned object: each key is a logical name, value is a full [Parameter Object](parameters.md). Reference in paths/operations with `$ref: "#/parameters/name"`.

## Example

```yaml
parameters:
  skipParam:
    name: skip
    in: query
    description: number of items to skip
    required: true
    type: integer
    format: int32
  limitParam:
    name: limit
    in: query
    description: max records to return
    required: true
    type: integer
    format: int32
  idParam:
    name: id
    in: path
    required: true
    type: string
    description: Resource ID
```

## Using in operations

```yaml
paths:
  /pets:
    get:
      parameters:
        - $ref: "#/parameters/skipParam"
        - $ref: "#/parameters/limitParam"
      responses: { ... }
  /pets/{id}:
    get:
      parameters:
        - $ref: "#/parameters/idParam"
      responses: { ... }
```

Path-level `parameters` also accept `$ref`; they apply to all operations on that path unless overridden.

## Key points

- Root `parameters` is a **library** of definitions only; no parameter is applied globally.
- Uniqueness (name + in) is per operation: you can mix inline parameters and `$ref`; no duplicate name+in in the same operation.
- Use for common query/path/header params (e.g. pagination, API key, tenant id) to keep the spec DRY.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
