---
name: core-info-metadata
description: Info, Contact, License, and API metadata in Swagger 2.0
---

# Info and Metadata Objects

## Info Object

Required at root. Provides API metadata.

| Field         | Type   | Required | Description |
|---------------|--------|----------|-------------|
| title         | string | Yes      | Application title. |
| version       | string | Yes      | API version (not spec version). |
| description   | string | No       | Short description; GFM allowed. |
| termsOfService | string | No      | Terms of service URL. |
| contact       | Contact Object | No | Contact for the API. |
| license       | License Object | No | License for the API. |
| ^x-           | Any    | No       | Vendor extensions. |

## Contact Object

| Field | Type   | Description |
|-------|--------|-------------|
| name  | string | Contact person/org. |
| url   | string | URL (must be valid URL). |
| email | string | Email (must be valid email). |

## License Object

| Field | Type   | Required | Description |
|-------|--------|----------|-------------|
| name  | string | Yes      | License name. |
| url   | string | No       | License URL. |

## Example

```yaml
info:
  title: Swagger Sample App
  description: Sample Petstore server.
  termsOfService: http://swagger.io/terms/
  contact:
    name: API Support
    url: http://www.swagger.io/support
    email: support@swagger.io
  license:
    name: Apache 2.0
    url: http://www.apache.org/licenses/LICENSE-2.0.html
  version: "1.0.1"
```

## Key points

- `version` is the **API** version, not the Swagger version (that is `swagger: "2.0"`).
- Description fields support GitHub Flavored Markdown.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
