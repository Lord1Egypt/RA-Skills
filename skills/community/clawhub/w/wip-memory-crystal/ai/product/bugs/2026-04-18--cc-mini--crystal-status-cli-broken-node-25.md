# `crystal status` (and all CLI entrypoints) broken on global install

**Filed:** 2026-04-18 PST
**Severity:** High for observability ... ingestion unaffected
**Status:** Fix prepared in this PR (tsup `noExternal` + build). Awaiting merge + release.

## Symptom

Running any `crystal` CLI subcommand from a global npm install throws at startup:

```
Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'dream-weaver-protocol'
  imported from /opt/homebrew/lib/node_modules/@wipcomputer/memory-crystal/dist/cli.js
```

Discovered 2026-04-18 while diagnosing Memory Crystal health on Parker's Mac mini running **Node 25.6.0** with `@wipcomputer/memory-crystal@0.7.34-alpha.5` (the version on npm at time of discovery).

Ingestion continues to work because it runs via the Claude Code Stop hook (`dist/cc-hook.js`) which is a different entrypoint — `cc-hook` does not import `dream-weaver-protocol`, so it resolves cleanly. Every `crystal <verb>` command run by the user, however, goes through `dist/cli.js` and fails immediately.

## Root cause

`package.json` declares the dep as a relative file path:

```json
"dream-weaver-protocol": "file:../dream-weaver-protocol-private"
```

This is correct for local development (sibling-directory layout on Parker's machine) but invalid when the package is published to npm. When `npm install -g @wipcomputer/memory-crystal` runs, npm tries to resolve `file:../dream-weaver-protocol-private` relative to the install root (`/opt/homebrew/lib/node_modules/@wipcomputer/memory-crystal/`). There is no `../dream-weaver-protocol-private` directory next to the global install, so npm either:
- leaves `node_modules/dream-weaver-protocol/` empty (no `package.json` inside), or
- fails silently and the dir is missing entirely.

Either way, when `dist/cli.js` hits `import { ... } from 'dream-weaver-protocol'`, Node 25's strict ESM resolver cannot find a package manifest and throws.

On earlier Node (pre-22, pre-strict), non-resolving bare imports sometimes worked via legacy loader quirks. Node 25.6 enforces the spec. This is why the break surfaced now even though the file: dep has always been there.

## Why the dep is a `file:` path in the first place

`dream-weaver-protocol-private` is not published to npm. It lives only as a sibling repo at `~/wipcomputerinc/repos/ldm-os/components/dream-weaver-protocol-private/`. The memory-crystal package imports its consolidation engine from dream-weaver-protocol for the `crystal dream` command.

Publishing dream-weaver-protocol to npm is on the priorities roadmap (see `wip-ldm-os-private/ai/product/product-ideas/vision-quest-01/priorities-2026-04-16.md` §3.3 "Dream Weaver skill bundle (P1, first marketplace submission)"), but it has not shipped yet.

## Fix in this PR

Add `tsup.config.ts` with:

```ts
export default defineConfig({
  noExternal: ['dream-weaver-protocol'],
});
```

This tells tsup to bundle `dream-weaver-protocol`'s source directly into every memory-crystal dist entrypoint that imports it. After the build, `dist/cli.js` (and the other entrypoints) contain the dream-weaver code inline and no longer emit the bare `from 'dream-weaver-protocol'` import. The published package is self-contained.

Verified locally: `grep -c 'from "dream-weaver-protocol"' dist/cli.js` returns 0 after rebuild, and `node dist/cli.js status` runs cleanly and reports 92,696 chunks.

Tradeoff: each of the ~24 entrypoints gets its own copy of the dream-weaver code, so `dist/` grows a few KB. Acceptable cost for a one-command crystal install that works on any Node version on any user's machine.

## Related (why this didn't surface sooner)

- Parker's prior Node version resolved the empty module path loosely.
- Most of Parker's day-to-day crystal access is via the MCP server (`dist/mcp-server.js` path, spawned by OC or Claude Code) OR the Stop hook (`dist/cc-hook.js`). Neither touches `dream-weaver.ts`, so no user-visible break.
- `crystal status` is the command a human runs when they want to confirm health. Exactly the command that broke.

## Follow-up work (separate bugs)

1. **Publish `dream-weaver-protocol` to npm** as a real package so it can be a regular semver dep of memory-crystal. That removes the need for the bundle-into-dist workaround. Tracks against priorities §3.3.
2. **Release pipeline check: bundle-check on dist before publish.** A pre-publish hook that runs `grep -l 'from "file:' dist/*.js` and blocks publish if anything still has a file-path bare import would catch this class of issue before it reaches npm.
3. **Node-version compatibility matrix in CI.** Run smoke tests against Node 18, 20, 22, 24, 25 so strict-ESM regressions fire at PR time.

## Acceptance

- [ ] This PR merged, memory-crystal released (patch bump, e.g. 0.7.34-alpha.5 → 0.7.35 or 0.7.34 stable)
- [ ] `npm install -g @wipcomputer/memory-crystal@<new>` on Parker's Mac mini
- [ ] `crystal status` runs cleanly, reports chunk count
- [ ] `crystal doctor` also runs cleanly (same entrypoint family)
- [ ] All other CLI verbs smoke-tested: `status`, `doctor`, `search "foo"`, `sources status`
