# Endpoint Design Rules

## URL and Method Conventions

- Use nouns for resources: `/users`, `/orders/{order_id}`.
- Prefer plural collections.
- Use `GET`, `POST`, `PATCH`, `PUT`, and `DELETE` with strict semantics.

## Response Shape

Use consistent wrappers where needed, but do not over-wrap simple resources.

```json
{
  "data": {
    "id": "usr_123",
    "email": "user@example.com"
  }
}
```

For list endpoints, include pagination metadata:

```json
{
  "data": [],
  "pagination": {
    "next_cursor": "abc",
    "has_more": true
  }
}
```

## Status Code Policy

- `200` for successful reads and updates.
- `201` for creates with created resource.
- `204` for successful deletes without body.
- `400` for invalid input.
- `401` for missing or invalid auth.
- `403` for authenticated but forbidden.
- `404` for missing resource.
- `409` for version or state conflicts.
- `422` for semantically invalid payloads.
- `429` for rate-limit enforcement.
- `5xx` for server-side failures.

## Idempotency

Require idempotency keys for unsafe, retry-prone create operations such as payments or provisioning.

## Filtering and Sorting

- Whitelist query parameters.
- Document supported operators.
- Reject unknown query keys to avoid silent bugs.
