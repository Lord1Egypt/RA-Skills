---
name: path-item-ref
description: Path Item $ref and external path definition in Swagger 2.0
---

# Path Item $ref

A [Path Item Object](paths-and-operations.md) can be defined **externally** using the `$ref` field. The referenced structure MUST be a valid Path Item Object (same format as inline path items).

## Fixed field

| Field | Type   | Description |
|-------|--------|-------------|
| $ref  | string | Reference to an external Path Item. Must resolve to a Path Item Object. |

When `$ref` is present, the Path Item is fully defined by the reference. Any other fields (get, put, parameters, etc.) in the same object are **not** combined with the reference; the spec says that if there are conflicts between the referenced definition and this Path Item's definition, the behavior is **undefined**. So in practice, use either `$ref` alone or inline path item fields, not both.

## Use cases

- **Reuse:** Same path structure (e.g. same path-level parameters) defined once and referenced from multiple path keys.
- **Split files:** Path Item stored in another file and referenced by path (e.g. `$ref: "paths/pet.yaml"`).

## Example

```yaml
paths:
  /pets/{id}:
    $ref: "#/paths/petById"
```

With root-level or external definition of `paths/petById` as a full Path Item (get, put, parameters, etc.). Note: the spec does not define a root `paths` key for reuse; this is an illustration. In practice, external file refs like `$ref: "pet-path.yaml"` are used.

## Key points

- Referenced value MUST be a [Path Item Object](paths-and-operations.md) (get, put, post, delete, options, head, patch, parameters, ^x-).
- Do not mix `$ref` with other Path Item fields on the same object; behavior is undefined on conflict.
- Useful for multi-file specs or shared path definitions.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
