---
name: core-tags-and-external-docs
description: Tag Object and External Documentation Object in Swagger 2.0
---

# Tags and External Documentation

## Tag Object

At root under `tags`. Adds metadata to tags used in Operation Object. Not every tag used in operations must be declared; undeclared tags may be ordered arbitrarily by tools. Tag names in the list MUST be unique.

| Field        | Type   | Required | Description |
|--------------|--------|----------|-------------|
| name         | string | Yes      | Tag name. |
| description  | string | No       | Short description; GFM allowed. |
| externalDocs | External Documentation Object | No | Extra docs. |
| ^x-          | Any    | No       | Extensions. |

## External Documentation Object

Used at root (`externalDocs`), in Info (not in 2.0), Operation, Tag, or Schema.

| Field       | Type   | Required | Description |
|-------------|--------|----------|-------------|
| description | string | No       | Short description; GFM allowed. |
| url         | string | Yes      | URL for the documentation. |

## Example

```yaml
tags:
  - name: pet
    description: Pets operations
    externalDocs:
      description: Find more info
      url: https://swagger.io
  - name: store
    description: Store operations
```

Operations reference tags by name in the `tags` array (e.g. `tags: [pet]`).

## Key points

- Tags group operations in UI; order in root `tags` can affect display order.
- External docs link out to detailed guides; use for long-form content.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
