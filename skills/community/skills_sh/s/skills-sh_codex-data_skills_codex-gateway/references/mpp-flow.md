# MPP Auth Flow Reference

## Auth matrix (MPP mode)

| Mode | Headers | Supports | Notes |
| ---- | ------- | -------- | ----- |
| MPP | `Authorization: Payment <credential>` | query only | `402` challenge/credential flow |

## Details

- Initial unpaid query returns `402` with multiple `WWW-Authenticate: Payment ...` challenges.
- Retry with `Authorization: Payment <credential>`.
- Success returns GraphQL data + `Payment-Receipt`.
- Mutation/subscription in MPP mode returns `403`.
- Valid API key/bearer auth takes precedence over the payment flow.

## Common failures

| Symptom | Likely cause | Fix |
| ------- | ------------ | --- |
| 402 + `WWW-Authenticate` | MPP challenge required | Solve one challenge and retry with `Authorization: Payment ...` |
| 402 + `malformed-credential` | Bad base64url or JSON credential | Rebuild credential payload |
| 402 + `invalid-challenge` | Unknown/expired/used challenge | Re-request and solve a fresh challenge |
| 402 + `verification-failed` | Payment proof rejected | Recreate proof for the returned challenge |
| 403 in MPP mode | Mutation or subscription attempt | Use API key/bearer auth for non-query operations |
