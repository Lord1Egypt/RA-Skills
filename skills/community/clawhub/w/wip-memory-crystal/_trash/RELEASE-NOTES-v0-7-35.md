# Memory Crystal v0.7.35

One-line release: **`crystal status` and every other CLI verb now actually run on global installs under modern Node**. Before this release, a silent packaging mistake made every `crystal <verb>` command throw `ERR_MODULE_NOT_FOUND` at startup on Node 25.6+, which is the first Node version to enforce strict ESM resolution against an unresolvable bare import. Ingestion continued to work the whole time because the Claude Code Stop hook takes a different code path.

## What was wrong

`package.json` declared its dream-weaver-protocol dependency with a `file:` relative path intended for local dev (`file:../dream-weaver-protocol-private`). When users ran `npm install -g @wipcomputer/memory-crystal`, npm tried to resolve that path relative to the global install root, could not find the sibling directory, and left the module unresolvable. Older Node resolvers tolerated the resulting empty state; Node 25 does not. Any entrypoint that imports `dream-weaver.ts` — which is every interactive CLI — threw on startup.

## What changed

Added `tsup.config.ts` with `noExternal: ['dream-weaver-protocol']`. Tsup now bundles dream-weaver's source code into each memory-crystal dist entrypoint at build time, so the published tarball is self-contained and needs no runtime resolution of that dep. The CLI verbs work on any Node from 18 to 25+.

## What did not change

- Ingestion: the Claude Code Stop hook path was never broken. Continuous capture kept going at normal rate.
- Search: the MCP server entrypoint was never broken. Agents that use `crystal_search` through MCP were unaffected.
- Data: zero chunks were lost. Today's DB count is 92,696 and growing.

## Related bugs filed in this release

- `ai/product/bugs/2026-04-18--cc-mini--crystal-status-cli-broken-node-25.md` — this bug in full, with root cause, discovery narrative, and follow-up work
- `ai/product/bugs/2026-04-18--cc-mini--lesa-capture-gap-2026-04-17.md` — a separate concern: during the Opus 4.7 rollout incident on Apr 17, Lēsa's gateway failed repeatedly on an unknown model ID and emitted no successful agent_end events, so ingestion for that day dropped to ~46 chunks vs ~300 baseline. Propose backfill + structural prevention in that bug.

## Install

```bash
npm install -g @wipcomputer/memory-crystal@latest
crystal status
```

If that reports your chunk count and agent list cleanly, you're on the fix.

Closes wipcomputer/memory-crystal#68.
