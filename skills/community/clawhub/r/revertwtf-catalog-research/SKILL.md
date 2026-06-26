---
name: revertwtf-catalog-research
description: Perform broader source-backed catalog enrichment for new EVM ecosystems, protocols, providers, standards, or deprecated/renamed/sunsetting coverage.
version: 0.1.0
---

# revert.wtf Catalog Research Skill

Use this skill for broad catalog coverage passes: new chains, protocol ecosystems, contract repositories, provider APIs, standards, x402-style flows, explorer APIs, or lifecycle audits.

## Research Standard

- Prefer primary sources: official specs, protocol docs, contract repositories, API docs, EIPs/ERCs, release notes, and verified source repositories.
- For current ecosystem status, verify live/current sources before marking something current, renamed, legacy, or sunsetting.
- Keep historical coverage when old contracts can still emit errors. Mark it `legacy`; do not delete useful entries just because the product is deprecated.
- Distinguish:
  - `legacy`: deprecated, wound down, or historical but still useful.
  - `sunsetting`: active enough to matter but tied to an announced shutdown date.
  - `renamed`: ecosystem branding changed while errors remain relevant.

## Workflow

1. Define the coverage target and scope.
2. Inventory current coverage:
   - Search shards in `packages/catalog/src/data/shards/`.
   - Check `packages/catalog/src/sources.ts` for lifecycle metadata.
   - Check generated selectors in `packages/selectors/src/generated.ts` when custom errors are involved.
3. Gather source material and record references in entries or `sources.ts`.
4. For Solidity custom errors, prefer using `scripts/enrich-new-ecosystem-shards.mjs` when the target fits its model.
5. Hand-author protocol/provider/API entries when errors are not Solidity custom errors.
6. Regenerate catalog data, run validation, and run the duplicate audit.

## Quality Bar

- Entries should be integration-useful, not merely encyclopedic.
- `nextSteps` should tell an app, wallet, support console, or agent what to do next.
- Avoid "retry later" as a default. Be specific about when retry helps.
- Avoid adding entries from random forum posts unless they are backed by code, docs, or repeated real-world artifacts.
- Avoid massive false-positive substring patterns.

## Verification

```bash
node scripts/build-catalog-data.mjs --generate --dist --check
node --experimental-strip-types scripts/validate-catalog.ts
node scripts/check-catalog-duplicates.mjs --fail-on=id,same-source-selector
node node_modules/typescript/bin/tsc -p packages/catalog/tsconfig.json --noEmit
node node_modules/typescript/bin/tsc -p packages/parser/tsconfig.json --noEmit
```

Useful smoke checks:

```bash
node --input-type=module -e "import { getCatalog } from './packages/catalog/dist/index.js'; console.log(getCatalog().length)"
```

If generated source files or dist JSON change, keep them synchronized with the shard source.
