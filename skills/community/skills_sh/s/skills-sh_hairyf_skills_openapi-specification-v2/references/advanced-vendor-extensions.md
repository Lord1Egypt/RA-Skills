---
name: advanced-vendor-extensions
description: Vendor extensions (x-) in Swagger 2.0
---

# Vendor Extensions (x-)

Extensions allow additional data at certain points in the spec. They are **not** part of the core specification; tooling may or may not support them.

## Rules

- **Prefix:** Field name MUST begin with `x-` (e.g. `x-internal-id`, `x-tag-groups`).
- **Value:** Can be `null`, a primitive, an array, or an object (any valid JSON value).
- **Where:** Many objects support patterned field `^x-`, meaning any key starting with `x-` is allowed. Check each object (Swagger Object, Info, Path Item, Operation, Parameter, Response, Schema, Tag, etc.) for "Patterned Objects" / "^x-".

## Examples

```yaml
paths:
  /pets:
    x-internal: true
    get:
      operationId: getPets
      x-rate-limit: 100
      responses:
        "200":
          description: OK
          x-example-id: pet-1
```

```yaml
info:
  title: My API
  version: "1.0"
  x-team: platform
  x-support-email: api@example.com
```

## Key points

- Use `x-` for tool-, vendor-, or project-specific metadata without breaking standard validators.
- Validators that don't know an extension typically ignore it (or treat as optional).
- Common conventions: `x-examples`, `x-code-samples`, `x-deprecated`, `x-internal`, `x-tag-groups`.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
