# HLN API Endpoints

## Base URLs

- Production API: `https://api.hlnames.xyz/`
- Production Swagger docs: `https://api.hlnames.xyz/api/docs/`
- Testnet API: `https://api.testnet.hlnames.xyz/`

The Swagger UI is publicly browsable without an API key. API routes still require `X-API-Key`.

## Endpoint Catalog

| Goal | Method + Path | Input | Response Notes |
| --- | --- | --- | --- |
| Hash a domain | `GET /utils/namehash/:domain` | `.hl` domain | Returns `{ "nameHash": "0x..." }` |
| Check registration | `GET /utils/registered/:nameHashOrId` | nameHash or tokenId | Returns `{ "registered": true|false }` |
| List names | `GET /utils/all_names?begin=0&end=999` | optional range | Returns array of `{ name, namehash, tokenid }`; defaults to range `0..999` |
| List names for owner | `GET /utils/names_owner/:address` | address string | Prefer normalized addresses |
| List primary names | `GET /utils/all_primary_names?begin=0&end=999` | optional range | Returns array of `{ address, primaryName, namehash, tokenid }` |
| List primary names for addresses | `POST /utils/all_primary_names` | Optional JSON body `{ "addresses": ["0x..."] }` | Swagger documents an optional `addresses` array request body; do not combine it with `begin`/`end` because the server returns `400` |
| Resolve domain to address | `GET /resolve/address/:domain` | `.hl` domain | Returns `{ "address": "0x..." }` |
| Reverse-resolve address | `GET /resolve/primary_name/:address` | EVM address | Returns `{ "primaryName": "name.hl" }` |
| Fetch profile | `GET /resolve/profile/:address` | EVM address | Swagger shows `primaryName` and `avatar`; real responses may also surface additional user-controlled profile metadata |
| Fetch resolution history | `GET /resolve/past_resolved/:domain` | `.hl` domain | Returns array of `{ blockNumber, resolvedAddr }` |
| Fetch resolution history in range | `GET /resolve/past_resolved/:domain/:blockNumStart/:blockNumEnd` | `.hl` domain and numeric block range | Returns array of `{ blockNumber, resolvedAddr, previousResolvedAddr? }` |
| Fetch expiry | `GET /metadata/expiry/:nameHashOrId` | nameHash or tokenId | Returns `{ "expiry": "1771416632" }` as a stringified number |
| Fetch full record | `GET /records/full_record/:nameHashOrId` | nameHash or tokenId | Returns `{ name, data }` with text records and `chainAddresses` |
| Fetch rendered image | `GET /records/image/:tokenId` | tokenId | Returns `{ "image": "data:image/svg+xml;base64,..." }` |
| Fetch supported coin types | `GET /records/coin_types` | none | Returns `{ "coinTypes": [0, 60, 501] }` |
| Mint-pass signing | `POST /sign_mintpass/:label` | label path param | Returns `{ label, sig, timestamp, token, amountRequired }` per the Swagger example |

## Public Docs Baseline

- Swagger examples are intentionally illustrative, not exhaustive.
- Data Records are user-controlled. Treat additional returned metadata fields as valid unless the API indicates an error.
- Suggested/default-style Data Records called out in the consulted docs and session include `Avatar`, `Twitter` or `X`, `Discord`, `Bio`, `REDIRECT`, and `CNAME`.

## Response Interpretation Notes

- `resolve/profile` is the best single-call profile lookup when the user starts from an address.
- Swagger’s example for `resolve/profile` is minimal. In practice, this route may surface additional user-controlled profile metadata beyond `primaryName` and `avatar`.
- `records/full_record` is the richest public response. It contains:
  - `name.owner`
  - `name.controller`
  - `name.resolved`
  - `name.name`
  - `name.expiry`
  - `data.records`
  - `data.chainAddresses`
- Interpret `data.records` as the free-form, user-controlled metadata dictionary.
- Interpret `data.chainAddresses` as the separate structured address map keyed by coin type, not as part of the text-record schema.
- `records/image` requires a tokenId, not a nameHash. Convert first if needed.
- `metadata/expiry` currently returns `"0"` for unregistered names rather than a successful-looking future timestamp.

## Practical Call Patterns

- Need profile data from an address:
  - Call `GET /resolve/profile/:address`
- Need the complete Data Records map or chain addresses for a name:
  - Call `GET /utils/namehash/:domain`
  - Then call `GET /records/full_record/:nameHashOrId`
- Need owner or list queries:
  - Call `GET /utils/names_owner/:address`, `GET /utils/all_names`, or `GET|POST /utils/all_primary_names`
- Need primary names for a specific address set:
  - Call `POST /utils/all_primary_names` with JSON body `{ "addresses": ["0x...", "0x..."] }`
  - Do not send `begin` or `end` in the same request
- Need historical resolution context:
  - Call `GET /resolve/past_resolved/:domain/:blockNumStart/:blockNumEnd`
  - Use `previousResolvedAddr` to describe transitions
- Need a minting preflight:
  - Validate the label first
  - Confirm the developer is ready to continue promptly into the mint transaction
  - Call `POST /sign_mintpass/:label`
  - Expect Swagger’s documented response fields: `label`, `sig`, `timestamp`, `token`, and `amountRequired`
  - Treat the payload as short-lived input for immediate onchain minting rather than a long-lived credential
