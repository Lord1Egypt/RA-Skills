---
name: advanced-extensions-and-xml
description: Vendor extensions (x-), Security filtering, and XML Object in Swagger 2.0
---

# Extensions, Security Filtering, and XML

## Vendor Extensions (x-)

Any field name starting with `x-` is an extension. Value can be null, primitive, array, or object. Example: `x-internal-id`, `x-tag-groups`. Tooling may or may not support them; specs can use them for custom needs.

## Security Filtering

Some objects may be empty or omitted for access control over the doc:

1. **Paths Object empty** — Viewer reached the right place but sees no paths; Info still visible (e.g. auth instructions).
2. **Path Item Object empty** — Path exists but operations/parameters hidden (finer control than hiding the path).

Not part of the spec itself; libraries may implement this behavior.

## XML Object

Used inside Schema Object (typically on properties) to describe XML representation. Ignored on root schema.

| Field     | Type    | Description |
|-----------|---------|-------------|
| name      | string  | Element/attribute name override. For array items: name of each element; for array with wrapped: true, name of wrapper. |
| namespace | string  | Namespace URL. |
| prefix    | string  | Namespace prefix. |
| attribute | boolean | true = render as attribute; default false. |
| wrapped   | boolean | For arrays only: true = wrapped element (e.g. &lt;books&gt;&lt;book/&gt;&lt;book/&gt;&lt;/books&gt;); default false. |

Array behavior: without `items.xml.name` and `xml.wrapped`, multiple sibling elements; with `items.xml.name`, that name for each item; with `xml.wrapped: true`, outer wrapper name from `xml.name` (or same as items if not set).

## Key points

- Use `x-` for tool- or vendor-specific metadata without breaking standard validators.
- Security filtering is a documentation/ACL pattern, not a schema requirement.
- XML Object is for APIs that expose or consume XML; optional for JSON-only APIs.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
