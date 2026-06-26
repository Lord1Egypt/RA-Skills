---
name: revertwtf-mcp-server
description: Maintain or use the read-only revert.wtf MCP server that exposes bounded catalog search, parser, selector lookup, AA explanations, x402 entries, and Blockscout registry tools to agents.
version: 0.1.0
---

# revert.wtf MCP Server Skill

Use this skill when changing `packages/mcp`, testing MCP behavior, documenting agent integration, or helping an agent consume revert.wtf data through MCP.

## Product Intent

- The MCP server is open source and free.
- It is for agents that encounter an EVM/RPC/provider/wallet/AA/x402 error and need catalog-backed help instead of broad internet searching.
- It is read-only. Do not add signing, sending transactions, payment gating, chain calls, browser scraping, or provider fetches to MCP behavior.
- It must never require clients to download the full catalog for simple lookup/search. Search tools return bounded summaries; full entries are fetched by id.

## Current Tools

- `explain_error`
- `decode_revert_data`
- `search_catalog`
- `get_error`
- `catalog_stats`
- `list_sources`
- `lookup_selector`
- `explain_aa_error`
- `get_blockscout_chain`
- `search_blockscout_chains`

## Current Resources

- `revertwtf://catalog/stats`
- `revertwtf://catalog/sources`
- `revertwtf://catalog/errors/{id}`
- `revertwtf://catalog/sources/{source}`
- `revertwtf://blockscout/chains/{chainId}`

## Implementation Rules

- Reuse precise package subpaths when possible: `@revertwtf/parser/explain`, `@revertwtf/parser/decode`, `@revertwtf/aa/explain`, and selector/catalog APIs.
- Keep tool outputs JSON text for broad client compatibility.
- Keep resource payloads JSON with `application/json`.
- Keep input schemas explicit and small. Add `limit`/`offset` to list/search tools and cap maximum result counts.
- `search_catalog` must return summary rows plus resource URIs, not full entries. Agents should call `get_error` only for a selected id.
- `list_sources` and `search_blockscout_chains` should stay paginated.
- Preserve clear errors for unknown ids, invalid selectors, or missing resource params.
- Update `packages/mcp/README.md` and `docs/mcp-server.md` when the tool/resource surface changes.

## Tests And Checks

Prefer in-memory MCP tests, not child-process stdio tests, because Windows local runs can hit `spawn EPERM`.

```bash
pnpm --filter @revertwtf/mcp test
pnpm --filter @revertwtf/mcp build
node node_modules/typescript/bin/tsc -p packages/mcp/tsconfig.json --noEmit
```

If testing stdio startup manually:

```bash
pnpm --filter @revertwtf/mcp build
pnpm --filter @revertwtf/mcp start
```

Do not leave a long-running MCP server process behind after smoke testing.
