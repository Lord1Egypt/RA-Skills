# API Contract Workflow

Use this flow to define a REST API before writing server code.

## 1. Model Resources and Ownership

- List core resources and their owners.
- Define canonical identifiers and immutable fields.
- Separate client-facing models from internal persistence models.

## 2. Define Endpoints by User Job

For each endpoint, specify:

- Method and path
- Request schema and validation rules
- Response schema for success
- Error schema and status code map
- Authorization requirement

## 3. Standardize Errors

Adopt one error envelope for all endpoints:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User not found",
    "request_id": "req_123",
    "details": []
  }
}
```

Keep `code` stable for machine handling, and `message` clear for humans.

## 4. Add Compatibility Rules

- Additive changes are allowed in minor versions.
- Breaking changes require new versioned routes or explicit migration windows.
- Deprecations must include sunset date and migration guidance.

## 5. Publish Contract Gates

Do not ship endpoints until all are true:

- OpenAPI validates without errors.
- Examples match actual implementation.
- Error codes are documented and tested.
- Security requirements are attached per operation.
