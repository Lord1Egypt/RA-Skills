# HyperEVM dApp Integration

Use this reference when the user is integrating HL Names into a HyperEVM dApp, wallet connection flow, or minting flow.

## Quick Workflow

1. Default read-only integration work to the production API:
   - `https://api.hlnames.xyz/`
   - Swagger docs: `https://api.hlnames.xyz/api/docs/`
2. Use the published example pair from the GitBook docs for smoke tests:
   - `testooor.hl`
   - `0xF26F5551E96aE5162509B25925fFfa7F07B2D652`
3. Pick the narrowest endpoint for the product surface:
   - Name input to address: `GET /resolve/address/:domain`
   - Wallet address to primary name or profile: `GET /resolve/profile/:address`
   - Full Data Records map, chain addresses, ownership, or expiry: `GET /records/full_record/:nameHashOrId`
   - Owner or list queries: `GET /utils/names_owner/:address`, `GET /utils/all_names`, `GET|POST /utils/all_primary_names`
4. Treat returned metadata as user-controlled profile data.
   - Common suggested/default-style keys include `Avatar`, `Twitter` or `X`, `Discord`, `Bio`, `REDIRECT`, and `CNAME`.
   - If the application needs the complete record set, follow `resolve/profile` with `records/full_record`.

## Wallet Integration

The GitBook wallet connector page documents two main paths:

- `@hlnames/rainbowkit`
  - For new projects: install `@hlnames/rainbowkit@latest` and use it where you would otherwise use `@rainbow-me/rainbowkit`.
  - For existing RainbowKit apps: install the HL Names fork of `@rainbow-me/rainbowkit@2.2.10` so current imports can stay unchanged.
  - Prefer the upstream-published GitHub install path or repository link when the goal is to follow the latest maintained HL Names integration.
- Dynamic
  - GitBook links to `https://github.com/ori-wagmi/hlnames_dynamic` for Dynamic-based integration.
  - Prefer the linked GitHub branch or repository reference when the goal is to follow the latest maintained integration example.

When the user asks for frontend wiring, start from the wallet stack they already use rather than inventing a custom resolution layer.

## REST API Notes

- The GitBook dApp integration page informs the REST API is intended for resolving names on both HyperEVM mainnet as well as HyperCore.
- For manual testing in Swagger UI, follow the current instructions on the GitBook dApp integration page.
- Keep API use read-only unless the user explicitly asks for mint-pass preparation.

## Minting Preflight

- `POST /sign_mintpass/:label` is the API preflight for third-party minting.
- The signature is valid for 1 minute, counting from the timestamp given in the response.
- Request it when the developer is ready to continue promptly into the mint transaction.
- Validate that the label is normalized and does not include the `.hl` suffix.
- The response is server-generated and intended for immediate use in the downstream mint call. If the mint is submitted after expiry, the onchain transaction should revert.

For end-to-end third-party minting examples, use the consulted public repo:
- `https://github.com/HLnames/hln_api_minting` (see README.md)
- Key example files:
  - `example/getSignedArgs.ts`
  - `example/getSignedArgs+Mint.ts`
  - `example/getSignedArgs+Mint.py`
- Treat this repo as the upstream reference point when the goal is to follow the latest maintained minting examples.

Use that repo when the user wants implementation examples for fetching signed arguments or continuing into the mint transaction flow.
