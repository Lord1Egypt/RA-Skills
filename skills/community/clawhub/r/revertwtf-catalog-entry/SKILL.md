---
name: revertwtf-catalog-entry
description: Add or update precise revert.wtf catalog entries, fixtures, source metadata, and matcher tests for one or a small set of EVM/RPC/provider/wallet/protocol errors.
version: 0.1.0
---

# revert.wtf Catalog Entry Skill

Use this skill when the task is to add, fix, rename, deprecate, or verify specific entries in the revert.wtf error catalog.

## Ground Rules

- Treat `packages/catalog/src/data/shards/` as the source of truth.
- Keep source IDs stable. Put display names, aliases, lifecycle labels, legacy/sunsetting/renamed notes, and source references in `packages/catalog/src/sources.ts`.
- Keep catalog, parser, MCP, CLI, and web result paths package-owned and reproducible.
- Prefer narrow evidence over broad matching. Avoid plain substrings for generated custom errors when a selector exists.
- Use `requires` for guard context, especially broad JSON-RPC codes like `-32000` or generic provider messages.

## Workflow

1. Inspect the raw error and classify it:
   - `layer`: `evm`, `rpc`, `provider`, `wallet`, `library`, `account_abstraction`, `protocol`, or `unknown`.
   - `source`: ecosystem/library/provider/protocol id.
   - `category`: stable free-form bucket such as `revert`, `json_rpc`, `gas_estimation`, `facilitator_verify`, or `signature`.
2. Choose the shard:
   - Core standards/providers go under `packages/catalog/src/data/shards/core/`.
   - Protocol/app/ecosystem contracts go under `packages/catalog/src/data/shards/ecosystems/`.
3. Add a `CatalogEntry` with:
   - globally unique kebab-case `id`
   - human title
   - tight `patterns`
   - concise `summary`
   - concrete `likelyCauses`
   - action-oriented `nextSteps`
   - honest `retryHelpful`, `increasingGasHelpful`, and `confidence`
   - source-backed `references`
4. Add or update fixtures under `fixtures/<layer-or-source>/` when practical.
5. Add parser or catalog tests when behavior could regress.

## Pattern Choices

- Use `selector` for known custom error selectors.
- Use `json_path` for structured provider/MCP/facilitator fields such as `code`, `status`, `invalidReason`, or `errorReason`.
- Use `aa_code` for ERC-4337 AAxx codes.
- Use exact regexes for revert reason strings generated from source code.
- Use broad substrings only when the phrase is distinctive enough across the whole catalog.

## Verification

Run the smallest useful set:

```bash
node scripts/build-catalog-data.mjs --generate --dist --check
node --experimental-strip-types scripts/validate-catalog.ts
node scripts/check-catalog-duplicates.mjs --fail-on=id,same-source-selector
node node_modules/typescript/bin/tsc -p packages/catalog/tsconfig.json --noEmit
node node_modules/typescript/bin/tsc -p packages/parser/tsconfig.json --noEmit
```

If the change touches parser behavior, also run parser tests when the local environment allows it:

```bash
pnpm --filter @revertwtf/parser test
```

On this Windows workspace, recursive pnpm/Vitest or Next commands may fail with `spawn EPERM`. If that happens, fall back to direct `tsc` and targeted Node smoke checks, and report the limitation.
