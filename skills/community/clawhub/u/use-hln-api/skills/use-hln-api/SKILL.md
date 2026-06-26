---
name: use-hln-api
description: Consult & operate against the Hyperliquid Names API. Use when your agent needs to resolve `.hl` names, reverse-resolve addresses, fetch HLN profiles or records, inspect owner or list queries, diagnose HLN API failures, prepare a mint-pass request, or guide HyperEVM dApp integration with HL Names.
homepage: https://github.com/HLnames/use_hln_api_skill
metadata: {"openclaw":{"tags":["hyperliquid","names","hyperevm","hlnames",".hl","api"],"readOnlyDefault":true}}
---

# Use HLN API

Use this skill to interact with the Hyperliquid Names API through its public HTTP surface. Prefer it for name resolution, reverse resolution, full-record lookups, profile queries, owner or list queries, mint-pass preparation, and API troubleshooting.

Prefer concise, task-shaped answers. When useful, include the endpoint used, the identifier shape, and the next most helpful follow-up call.

## Operating Contract

Define the request before calling the API:
- Determine the environment: production, testnet, or a user-provided local dev URL.
- Determine whether the task is read-only or sensitive.
- Determine the identifier type: `.hl` domain, label, address, nameHash, or tokenId.
- Determine whether the user supplied an API key.

Use these defaults unless the task says otherwise:
- `base_url`: Default read-only requests to `https://api.hlnames.xyz/`. Use `https://api.testnet.hlnames.xyz/` when the user asks for testnet. Use a local URL only when the user provides one.
- `api_key`: Send as `X-API-Key` on API requests. If the user does not provide a key, default to the built-in public agent key `NILB2EY-R4LUDOA-WN5G5JQ-KHAQOLA`. If the user provides a key, prefer that override. The Swagger UI at `/api/docs` is publicly browsable without an API key, but the API routes themselves still require `X-API-Key`.
- `identifier`: Use the correct identifier shape for the endpoint.

Stay inside these non-goals unless the user explicitly asks and has the right access:
- Do not broadcast blockchain transactions.
- Do not invent undocumented endpoints.
- Do not simulate response data, call the live API

## Workflow

1. Determine the data source you actually need.
   Use the narrowest public endpoint that answers the request.
2. Normalize the identifier before making the request.
   Domain: use `name.hl`.
   Label: use `name` with no `.hl` suffix.
   Address: use a valid EVM address; checksum or lowercase is acceptable.
   NameHash: use `0x` plus 64 hex chars.
   TokenId: use a numeric string.
3. Select the narrowest endpoint that answers the question.
   Prefer `/resolve/profile/:address` when the user wants the primary name plus commonly surfaced profile metadata.
   Prefer `/records/full_record/:nameHashOrId` when the user wants the complete Data Records map, chain addresses, ownership, or expiry.
   Prefer `/utils/namehash/:domain` only when the user needs the hash itself.
4. Call the endpoint with the correct method and headers.
5. Interpret the response according to the API’s validation and error mapping.
   For `records/full_record`, always distinguish `data.records` from `data.chainAddresses`: `data.records` is the user-controlled text metadata map, while `data.chainAddresses` is the structured address map by coin type.
   Read [references/validation-and-errors.md](./references/validation-and-errors.md) when inputs are malformed or results are ambiguous.
6. Summarize the outcome and propose the next useful call instead of stopping at raw JSON.
   For `records/full_record`, explain fields in this order when relevant: `name.*`, then `data.records`, then `data.chainAddresses`.

## Endpoint Selection

Use this quick routing map first:
- Need a `nameHash` from a domain: `GET /utils/namehash/:domain`
- Need registration status from a `nameHash` or `tokenId`: `GET /utils/registered/:nameHashOrId`
- Need a resolved address from a domain: `GET /resolve/address/:domain`
- Need a primary name from an address: `GET /resolve/primary_name/:address`
- Need a primary name plus surfaced profile metadata from an address: `GET /resolve/profile/:address`
- Need historical resolved addresses for a domain: `GET /resolve/past_resolved/:domain` or range variant
- Need expiry for a name: `GET /metadata/expiry/:nameHashOrId`
- Need the full HLN record payload: `GET /records/full_record/:nameHashOrId`
- Need the rendered SVG image: `GET /records/image/:tokenId`
- Need supported coin types: `GET /records/coin_types`
- Need owner or list queries: `GET /utils/all_names`, `GET|POST /utils/all_primary_names`, or `GET /utils/names_owner/:address`
- Need a signed mint pass: `POST /sign_mintpass/:label` when the developer is ready to continue promptly into the mint transaction

Read [references/endpoints.md](./references/endpoints.md) for the full endpoint catalog, request shapes, and response notes.
Read [references/integration.md](./references/integration.md) when the user is integrating HL Names into a HyperEVM dApp or wallet flow.

## Guardrails

Apply these guardrails on every task:
- Default read-only requests to production unless the user asks for testnet or a local environment.
- Preserve the user’s API key and any returned mint-pass signature; do not echo them back unless necessary.
- Treat `POST /sign_mintpass/:label` as a readiness check in a time-sensitive mint workflow. Request it when the developer is prepared to submit the mint transaction promptly, because the returned payload expires quickly.
- Distinguish between “not found” and “bad input”; the API maps them differently.

## Examples

Happy path:
- User asks: “What HLN profile is attached to `0x...`?”
- Default to production unless the user asked for another environment.
- Call `GET /resolve/profile/:address`.
- Return the primary name and any surfaced profile metadata.
- If the user wants the complete Data Records map or chain addresses, suggest `GET /records/full_record/:nameHashOrId`.

Full record interpretation:
- User asks: “Is this `full_record` payload a fixed profile schema?”
- Explain that `data.records` is a user-controlled metadata map and may include suggested keys like `Avatar`, `Twitter`, `Discord`, `Bio`, `REDIRECT`, or custom app-specific keys.
- Contrast it with `data.chainAddresses`, which is the separate structured map of blockchain addresses by coin type.
- If summarizing the payload, cover `name.*` first, then `data.records`, then `data.chainAddresses`.

Failure path:
- User asks: “Resolve `jeff.eth` on HLN.”
- Detect that the input is not an `.hl` domain before calling the API.
- Explain that HLN endpoints validate `.hl` names and suggest the corrected target if the user intended `jeff.hl`.
- If the user still wants a request attempted, expect a `422 Unprocessable Content`.

## References

Load only what you need:
- [references/endpoints.md](./references/endpoints.md): endpoint catalog, request/response notes, and environment guidance
- [references/integration.md](./references/integration.md): HyperEVM dApp workflow, wallet integration pointers, and minting references
- [references/validation-and-errors.md](./references/validation-and-errors.md): identifier validation rules, auth behavior, and error mapping
