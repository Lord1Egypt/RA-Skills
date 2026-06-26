---
name: best-practices-spec-authoring
description: Practical authoring practices for Swagger 2.0 specs
---

# Best Practices (Spec Authoring)

## operationId

- **Use a unique operationId for every operation.** Many tools use it for method names and client generation.
- Prefer a clear, stable name (e.g. `getPetById`, `createOrder`). Avoid changing it across versions.

## Tags

- Use **tags** to group operations (e.g. by resource or feature). Declare tags at root with `name` and optional `description`/`externalDocs` for UI order and docs.
- Keep tag names short and consistent; operations can list multiple tags.

## Responses

- **Document at least one success response** (e.g. 200 or 201). The spec says operations SHOULD document success.
- Use **default** for unexpected or unspecified status codes (e.g. generic error schema).
- Reuse common responses via root `responses` and `$ref` (e.g. 404, 500, 400).

## Parameters

- **Path parameters:** Always set `required: true`; name must match the path segment.
- **Uniqueness:** (name, in) must be unique per operation; path-level and operation-level parameters merge, with operation overriding.
- Reuse common parameters (pagination, API key, etc.) via root `parameters` and `$ref`.

## Summary and description

- **summary:** Short line for UI; spec recommends under 120 characters.
- **description:** Use for behavior, constraints, and examples; GFM is supported.

## Definitions and schemas

- Put reusable models under **definitions** and reference with `$ref: "#/definitions/Name"`.
- For polymorphism use **discriminator** on the base schema and named definitions for each subtype; discriminator property must be in `required`.

## Security

- Declare schemes in **securityDefinitions**; apply at root (`security`) and/or per operation. Use `security: []` on an operation to clear root security.
- OAuth2: list required **scopes** in the Security Requirement Object; for apiKey/basic use empty array.

## Key points

- Prefer reuse (parameters, responses, definitions) to keep the spec maintainable and consistent.
- Use operationId + tags + clear responses so codegen and docs stay predictable.

<!--
Source references:
- https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md
-->
