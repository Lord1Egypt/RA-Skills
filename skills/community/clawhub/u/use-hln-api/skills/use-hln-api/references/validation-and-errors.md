# Validation And Errors

Use this file when an HLN request fails before or after hitting the API.

## Authentication

- Send the API key in the `X-API-Key` header.
- Expect `401` with this shape when the key is missing or wrong:

```json
{ "error": "Unauthorized: Invalid API Key" }
```

- Swagger UI at `/api/docs` requires no API-key auth.

## Identifier Rules

Validate locally before calling the endpoint when possible. Swagger documents the endpoint parameter shapes, and the notes below preserve the stricter current validation guidance already captured in this skill.

| Identifier | Current API rule | Failure detail |
| --- | --- | --- |
| Domain | String ending in `.hl`, total byte length `4..32` by current validator | `Domain not valid (1-31 chars + .hl suffix)` |
| Label | String without `.hl`, byte length `1..29` by current validator | `Label not valid (1-31 chars), no .hl suffix` |
| Address | Must pass `viem` `isAddress()` | `Valid EVM address is required.` |
| NameHash | `0x` plus 64 hex chars | `NameHash must be 0x-prefixed 32-byte hex string.` |
| TokenId | Numeric string | `TokenID must be a number.` |
| NameHashOrId | Valid nameHash or numeric tokenId | `NameHash must be 0x-prefixed 32-byte hex string or a valid TokenID.` |

## Error Mapping

The API normalizes many failures into structured `error` payloads.

| Status | Meaning | Typical Shape |
| --- | --- | --- |
| `400` | Bad request body or unsupported parameter combination | `{ "error": { "message": "Bad Request.", "details": "..." } }` or route-specific `{ "error": "..." }` |
| `401` | Missing or invalid API key | `{ "error": "Unauthorized: Invalid API Key" }` |
| `404` | Name not found or endpoint-specific absence | `{ "error": { "message": "...", "status": 404 } }` |
| `405` | Unsupported method on a route that falls through to method check | `{ "error": { "message": "Method Not Allowed.", "status": 405 } }` |
| `406` | Reserved fallback | `{ "error": { "message": "Not Acceptable.", "status": 406 } }` |
| `422` | Validation failure or invalid HLN argument | `{ "error": { "message": "Unprocessable Content.", "status": 422, "details": "..." } }` |
| `500` | Internal API or upstream failure | `{ "error": { "message": "...", "status": 500 } }` or route-specific `{ "error": "..." }` |

## Observed Semantics That Matter

- `NAME_NOT_REGISTERED` maps to `404`.
- `DOMAIN_NOT_HL` and `INVALID_ARGUMENT` map to `422`.
- Contract errors may bubble up through `metaMessages`; the API surfaces the first message containing `Error:`.
- `getExpiry()` returns `0` for unregistered names rather than throwing, so do not misread an expiry of `"0"` as a valid timestamp.

## Troubleshooting Checklist

1. Confirm the environment and base URL.
2. Confirm `X-API-Key` is present and valid.
3. Confirm the identifier matches the endpoint contract.
4. Distinguish direct validation failure (`422`) from absence (`404`).
5. For `POST /utils/all_primary_names`, do not combine address-body filtering with `begin` or `end`.
6. For `POST /sign_mintpass/:label`, confirm the label has no `.hl` suffix.
