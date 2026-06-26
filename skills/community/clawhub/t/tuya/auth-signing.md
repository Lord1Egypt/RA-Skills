# Tuya Auth and Signing Reference

Use this guide for all Tuya OpenAPI authentication and signature work.

## Project Prerequisites

- Tuya IoT Platform project created and authorized for required APIs.
- Access ID and Access Secret available locally.
- Correct data-center endpoint selected before requesting tokens.

## Regional OpenAPI Hosts

- China: `https://openapi.tuyacn.com`
- Europe: `https://openapi.tuyaeu.com`
- Europe West: `https://openapi-weaz.tuyaeu.com`
- US East: `https://openapi.tuyaus.com`
- US West: `https://openapi-ueaz.tuyaus.com`
- India: `https://openapi.tuyain.com`

## Token Workflow

1. Request project token with:
- `GET /v1.0/token?grant_type=1`
2. Cache token with expiration metadata.
3. Refresh token before expiry or on token-invalid response.

## Signature Inputs (HMAC-SHA256)

Tuya documents this request signature pattern:
- `sign = HMAC-SHA256(client_id + [access_token] + t + nonce + stringToSign, secret)`
- `stringToSign` includes method, body hash, signed headers, and URL path with query

For GET requests with empty body, body hash is SHA256 of empty string.

## Required Headers

- `client_id: <ACCESS_ID>`
- `t: <13-digit unix ms timestamp>`
- `sign_method: HMAC-SHA256`
- `sign: <computed signature>`
- `access_token: <token>` for service calls after token creation
- `nonce: <optional uuid>` when used in signature construction

## Validation Checklist Before Sending

- Endpoint host matches project data center.
- Timestamp generated at request time.
- Signed URL path and query exactly match outbound request.
- Body hash matches serialized payload bytes.
- Header order in signature input matches Tuya rule.

## Failure Patterns

- Wrong endpoint + valid credentials -> auth fails despite correct key pair.
- Mismatched body hash -> signature rejected.
- Replayed stale timestamp -> signature rejected.
- Missing `access_token` for protected endpoint -> unauthorized.
