---
name: core-swagger-object
description: Root Swagger object and required/optional fields for OpenAPI 2.0
---

# Swagger Object (Root)

Root of the API spec. Combines the former Resource Listing and API Declaration into one document.

## Required fields

| Field     | Type   | Description |
|----------|--------|-------------|
| swagger  | string | MUST be `"2.0"`. |
| info     | Info Object | API metadata. |
| paths    | Paths Object | Available paths and operations. |

## Optional fixed fields

| Field              | Type   | Description |
|--------------------|--------|-------------|
| host               | string | Host only (no scheme/path); MAY include port. No path templating. |
| basePath           | string | Path relative to host; MUST start with `/`. No path templating. |
| schemes            | [string] | `"http"`, `"https"`, `"ws"`, `"wss"`. |
| consumes           | [string] | Global MIME types consumed; overridable per operation. |
| produces           | [string] | Global MIME types produced; overridable per operation. |
| definitions       | Definitions Object | Data types produced/consumed. |
| parameters         | Parameters Definitions Object | Reusable parameters (not global for all ops). |
| responses          | Responses Definitions Object | Reusable responses (not global). |
| securityDefinitions | Security Definitions Object | Security scheme definitions. |
| security           | [Security Requirement Object] | API-wide security (OR between entries). |
| tags               | [Tag Object] | Tag list with metadata; order may be significant. |
| externalDocs       | External Documentation Object | Additional docs. |

## Patterned fields

- **Paths:** `/{path}` → Path Item Object. Path MUST begin with `/`; path templating allowed.
- **Extensions:** `^x-` (e.g. `x-internal-id`) — any JSON value; vendor-specific.

## Example (minimal)

```yaml
swagger: "2.0"
info:
  title: My API
  version: "1.0.0"
paths:
  /pets:
    get:
      responses:
        "200":
          description: list of pets
```

## Key points

- `parameters` and `responses` at root define **reusable** definitions only; they do not apply globally to every operation.
- Top-level `security` is OR: any one of the listed requirement objects can satisfy it. Operations can override with their own `security` or use `[]` to clear.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
