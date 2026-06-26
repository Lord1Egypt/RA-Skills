---
name: revertwtf-agent-api
description: Use revert.wtf safely from agents, tools, browsers, or integrations through bounded HTTP APIs, MCP tools, and lightweight package subpaths without downloading the full catalog into client bundles.
version: 0.1.0
---

# revert.wtf Agent API Skill

Use this skill when an agent needs to explain an EVM/RPC/provider/wallet/AA/x402 error, resolve a selector, search the catalog, or integrate revert.wtf into a product.

## Default Choice

- Prefer MCP when the agent runtime supports MCP.
- Prefer the website HTTP API when calling the hosted service from an agent or app backend.
- Prefer package subpaths for local code.
- Never import the full catalog-backed parser into browser/client bundles for one-off searches.

## MCP Tools

Use bounded tools:

- `explain_error` for raw errors, traces, JSON strings, revert bytes, and x402 payloads.
- `search_catalog` for catalog discovery. It returns summaries with `limit`, `offset`, `totalMatches`, and `hasMore`.
- `get_error` only after `search_catalog` returns a specific id.
- `lookup_selector` for 4-byte selectors.
- `decode_revert_data` for raw revert bytes.
- `explain_aa_error` for AAxx and EntryPoint failures.
- `search_blockscout_chains` and `get_blockscout_chain` for Blockscout registry checks.

Do not request or construct an all-catalog dump. Page through summaries only when the user explicitly needs breadth.

## Hosted HTTP API

POST JSON to the public web API from a server/agent context:

```bash
curl -s https://revert.wtf/api/explain \
  -H "content-type: application/json" \
  -d '{"raw":"{\"code\":-32000,\"message\":\"nonce too low\"}"}'
```

Useful endpoints:

- `POST /api/explain` with `{ "raw": "..." }`
- `POST /api/revert-decode` with `{ "data": "0x...", "abiText": "[...]" }`
- `POST /api/aa-decode` with `{ "raw": "AA23 reverted or OOG" }`
- `POST /api/selector` with `{ "selector": "0x08c379a0" }`
- `POST /api/search` with `{ "query": "AA23", "limit": 20, "offset": 0 }`

Inputs are capped for parsing. Do not paste private keys, seed phrases, access tokens, unreleased exploit details, or personal data.

Use `/api/search` for discovery and `/api/explain` for a specific raw failure.
Search returns summaries; fetch or explain the selected item instead of asking
for broad payloads.

## Package Imports

Use precise subpaths:

```ts
import { explain } from "@revertwtf/parser/explain"; // server/API path
import { decodeRevertData } from "@revertwtf/parser/decode";
import { describePanic } from "@revertwtf/catalog/panic";
import { listKnownAACodes } from "@revertwtf/aa/parse";
import { searchCatalog } from "@revertwtf/search"; // server-side SQLite FTS
```

Browser/client bundles should use small helpers or call an API route. Full-data surfaces such as `@revertwtf/catalog`, `@revertwtf/parser/explain`, and `@revertwtf/aa/explain` belong on a server/API boundary.

For browser apps, prefer the lightweight SDK:

```ts
import { createRevertClient } from "@revertwtf/client";

const revert = createRevertClient();
const result = await revert.searchCatalog({ query: "x402 payment required", limit: 5 });
```
