---
name: revertwtf-parser-decoder
description: Modify or debug revert.wtf normalization, revert-data extraction, trace extraction, ABI decoding, catalog matching, selector lookup, or ERC-4337 decoding behavior.
version: 0.1.0
---

# revert.wtf Parser And Decoder Skill

Use this skill when working in `packages/parser`, `packages/selectors`, `packages/aa`, or shared result types in `packages/core`.

## Boundaries

- Parser behavior must stay reproducible from package data and caller-provided input.
- Keep live lookups out of parser paths.
- No website-only explanation logic in `packages/parser`.
- Website, CLI, MCP, and packages should consume the same parser/catalog results.
- Preserve evidence-based ranking. Specific decoded evidence should beat broad wrappers.
- Keep full catalog-backed surfaces on server/API boundaries. Do not make a browser client download the catalog for one decode/search.
- Use package subpaths for small imports: `@revertwtf/parser/decode`, `@revertwtf/parser/explain`, `@revertwtf/catalog/panic`, `@revertwtf/aa/parse`, `@revertwtf/aa/explain`.

## Parser Map

- `packages/parser/src/normalizeError.ts` collects messages, codes, error names, revert data, method/action hints, and trace frames.
- `packages/parser/src/extractRevertData.ts` finds revert bytes in nested provider and simulator payloads.
- `packages/parser/src/extractTraceFailures.ts` summarizes failed call frames.
- `packages/parser/src/decodeRevertData.ts` decodes Solidity `Error(string)`, `Panic(uint256)`, provided ABI errors, and selector catalog matches.
- `packages/parser/src/matchCatalog.ts` indexes and matches catalog patterns.
- `packages/parser/src/explain.ts` ranks decoded results, trace evidence, and catalog matches into user-facing explanations.
- `packages/parser/src/browser*.ts`, `packages/catalog/src/browser.ts`, and `packages/aa/src/browser*.ts` protect browser-condition imports from accidental full-data bundles.
- `packages/aa/src/` handles ERC-4337 AAxx and EntryPoint `FailedOp`/`FailedOpWithRevert`.

## Workflow

1. Reproduce with a fixture or minimal object.
2. Decide whether the issue belongs in:
   - normalization/extraction,
   - revert decoding,
   - catalog matching,
   - AA decoding,
   - selector data,
   - or catalog entry data.
3. Keep the behavioral change narrow and covered by tests.
4. Add fixtures for new provider shapes or revert payloads.
5. Avoid changing match priority globally unless a test proves the previous order was wrong.

## Tests And Checks

```bash
node node_modules/typescript/bin/tsc -p packages/core/tsconfig.json --noEmit
node node_modules/typescript/bin/tsc -p packages/selectors/tsconfig.json --noEmit
node node_modules/typescript/bin/tsc -p packages/parser/tsconfig.json --noEmit
node node_modules/typescript/bin/tsc -p packages/aa/tsconfig.json --noEmit
```

When the local runner allows it:

```bash
pnpm --filter @revertwtf/parser test
pnpm --filter @revertwtf/aa test
pnpm --filter @revertwtf/selectors test
```

If pnpm/Vitest fails with `spawn EPERM`, report that and include direct `tsc` plus a targeted Node smoke check.
