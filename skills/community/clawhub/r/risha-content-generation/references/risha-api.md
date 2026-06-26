# Risha API Reference

## Source

This reference was derived from the published Swagger 2.0 document at:

- `https://adminxcore-api.risha.ai/api/docs/?format=openapi`

The docs UI at `/api/docs/` links to a Django login page, but the OpenAPI document is still fetchable directly.

## Base API Settings

- Host: `adminxcore-api.risha.ai`
- Base path: `/api`
- Primary published security scheme: `Basic`
- Practical auth workflow: `/auth/login/` also exists and accepts an email/password payload

Because the login response schema is not described in OpenAPI, client code should support:

- a prebuilt auth header supplied by the caller
- cookie-based sessions when login sets cookies
- token extraction from common JSON keys such as `access`, `access_token`, `token`, or `jwt`

## Important Endpoints

### Auth

- `POST /auth/login/`
- `GET /auth/me/`
- `POST /auth/logout/`

Observed behavior:

- invalid login returns `400` with `{"non_field_errors":["Invalid email or password"]}`

### Capability Discovery

- `GET /customer/capabilities/`
- `GET /customer/capabilities/{id}/`
- `POST /customer/capabilities/{id}/calculate-credit-cost/`
- `GET /customer/capabilities/creator-choices/`

Use these before generation. The capability object includes a linked `manual`.

### Generation

- `POST /generation-requests/`
- `GET /generation-requests/`
- `GET /generation-requests/{id}/`
- `POST /generation-requests/{id}/cancel/`
- `POST /generation-requests/{id}/retry/`
- `GET /generation-requests/{id}/generated_content/`
- `GET /generated-content/`

### Credits

- `GET /credits/wallets/my-summary/`
- `POST /customer/capabilities/{id}/calculate-credit-cost/`

### Creator Management

- `GET /user-creators/`
- `POST /user-creators/`
- `POST /user-creators/{id}/upload-file/`
- `POST /user-creators/{id}/sync/`

### Chat

- `POST /chat/`
- `POST /chat/stream/`

The schema currently omits the request body definitions for these endpoints, so they are not the best starting point for deterministic automation.

## How To Build `prompt_data`

`POST /generation-requests/` accepts a body shaped like:

```json
{
  "capability": 123,
  "title": "Optional title",
  "prompt_data": {}
}
```

The OpenAPI contract does not describe the exact keys inside `prompt_data`. Instead, fetch the capability detail and inspect:

- `capability.manual.fields`

Each manual field provides the rules needed to construct valid payloads:

- `field_path`: nested destination such as `input.text`
- `json_type`: `string`, `number`, `integer`, `boolean`, `array`, `object`, or `file`
- `is_required`
- `choice_model`: one of `enum_values`, `dialects`, `voices`, `creators`
- `enum_values`
- validation ranges such as `min_value`, `max_value`, `min_length`, `max_length`
- file constraints such as `accepted_file_type` and `max_file_size`
- credit rules in `credit_costs`

### Nested Path Rule

Translate a field path into nested JSON. Example:

- `input.text` with value `"Launch campaign copy"` becomes:

```json
{
  "input": {
    "text": "Launch campaign copy"
  }
}
```

### Choice Rule

For choice-backed fields:

- use the live choice endpoints or the values embedded in the manual
- send the machine value, not the label

Examples:

- creators: use the `field_value` from `GET /customer/capabilities/creator-choices/`
- enum values: use the literal enum entry defined for the field

## Status Model

Generation requests and generated content use these statuses:

- `in_queue`
- `processing`
- `completed`
- `failed`
- `cancelled`

Poll until a terminal state is reached.

## Output Shape

Generated content may include:

- `content`: the main generated text
- `asset`: generated media metadata
- `thumbnail`: preview media metadata
- `content_metadata`: provider-specific structured extras

For text workflows, prefer `generated_content.content`.

## Known Gaps

- login success response schema is not documented
- chat request schema is not documented
- capability list schema does not fully inline `manual.fields` in the simple list response, so a detail fetch is safer than relying on the paginated list alone

## Recommended CLI Flow

1. `python3 scripts/risha_api.py me`
2. `python3 scripts/risha_api.py catalog --quiet --write-json references/current-capabilities.json --write-markdown references/current-capabilities.md`
3. `python3 scripts/risha_api.py capability <id>`
4. `python3 scripts/risha_api.py creators` when a creator-backed field is present
5. `python3 scripts/risha_api.py estimate --capability-id <id> --prompt-data-file /absolute/path/prompt.json`
6. `python3 scripts/risha_api.py generate --capability-id <id> --prompt-data-file /absolute/path/prompt.json --wait`

## Bundled Snapshot

This skill can carry a live-refreshed capability snapshot in:

- `references/current-capabilities.json`
- `references/current-capabilities.md`

That snapshot is the fastest way to make all accessible capabilities ready for later execution without rediscovering them one by one.
