---
title: "Installer: source.bundled for parent-package extensions (Step 2)"
status: open
priority: P2
owner: Installer Cody
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-05-13
---

# Installer: `source.bundled` for parent-package extensions

## Problem

Some extensions ship as components inside a larger npm package, not as standalone npm packages. The canonical example is `lesa-bridge`:

- Source lives at `wip-ldm-os-private/src/bridge/` (cli.ts, core.ts, mcp-server.ts, openclaw.ts).
- Built by the `build:bridge` npm script in `wip-ldm-os-private/package.json`.
- Deployed to `~/.ldm/extensions/lesa-bridge/` as a fully-formed extension (its own dist, inbox, MCP server, CLI bin).
- Versioned independently (currently `0.3.0`).
- **Not** published to npm as a standalone package. Ships only inside `@wipcomputer/wip-ldm-os`.

The deprecated repo `github.com/wipcomputer/wip-bridge-deprecated` carries the explicit note: "DEPRECATED. Bridge is now part of LDM OS (v0.3.0+)."

Same pattern as `@wipcomputer/wip-ai-devops-toolbox` bundling sub-tools (`wip-release`, `wip-license-hook`, etc.) inside its `tools/` directory.

Today's registry has no way to express "this extension ships with that parent package." `lesa-bridge` is currently tracked as `source.npm: "lesa-bridge"` which is wrong (no standalone npm package exists).

## Proposal

Add the `bundled` updateSource type to the registry schema (per the [parent design](2026-05-13--cc-mini--installer-registry-source-types-architecture.md)):

```jsonc
{
  "lesa-bridge": {
    "updateSource": { "type": "bundled", "ref": "@wipcomputer/wip-ldm-os" },
    "provenance": {
      "repo": "wipcomputer/wip-bridge-deprecated",
      "notes": "Bridge code moved into wip-ldm-os v0.3.0; original repo deprecated 2026-03-16."
    },
    "installed": { "version": "0.3.0" }
  }
}
```

`updateSource.ref` names the parent npm package that ships this extension. The optional `provenance` block carries any historical/origin info that's useful to humans but doesn't drive the probe.

### Audit gate (cross-repo scope)

Before this slice writes code, run an audit: which currently-installed extensions are actually bundled inside parent packages, and which just look bundled? The minimum scope for this slice is `lesa-bridge` (bundled in `@wipcomputer/wip-ldm-os`, confirmed). Anything else is **gated on audit findings** and may either land in this slice or get split into a separate ticket.

Cross-repo work, if needed, is the manifest contract below. **Audit determines whether `wip-ai-devops-toolbox` work lands here or as a follow-up.** This ticket does not commit to delivering toolbox bundled-subtools coverage in one slice; that risks scope creep that swallows multiple alphas.

### Bundled-children manifest contract (defined here, applied per audit findings)

Parents that bundle extensions declare their children explicitly in `package.json`:

```jsonc
{
  "name": "@wipcomputer/wip-ldm-os",
  "version": "0.4.85-alpha.27",
  "wipcomputer": {
    "bundledExtensions": ["lesa-bridge"]
  }
}
```

LDM OS reads `wipcomputer.bundledExtensions` from the installed parent's `package.json` at install time and writes `updateSource: { type: "bundled", ref: "<parent>" }` for each named child. No hardcoded allowlist; the contract is the manifest field.

Minimum scope of this slice: `wip-ldm-os-private/package.json` declares `wipcomputer.bundledExtensions: ["lesa-bridge"]`. LDM OS implements the read+register logic. Any audit-included parents in OTHER repos either land here (if the audit confirms they're in scope) or get their own follow-up ticket.

## `ldm status` behavior

When a registry entry has `updateSource.type: "bundled"`, status:

1. Does **not** directly probe npm for this extension's version.
2. Looks up the parent package (named in `updateSource.ref`) in the registry. If the parent has an update available (from the parent's own probe), the bundled extension's update status is implicitly "rebuilt with parent on next install."
3. Reports the row as something like:

```
lesa-bridge        v0.3.0     (bundled with @wipcomputer/wip-ldm-os, updates via parent)
```

4. If the parent has no update available, the bundled extension is implicitly current.
5. If the parent is itself bundled (chained bundling), follow the chain to the root parent. Cycles should be detected and reported as a registry error.

## How `ldm install` populates the bundled type

When `ldm install <parent-package>` deploys a parent, the install code reads `wipcomputer.bundledExtensions` from the parent's `package.json`. For each child name in that array, when the corresponding sub-extension gets registered, the registry entry is written with `updateSource: { type: "bundled", ref: "<parent>" }`.

For `lesa-bridge` specifically, this happens during `ldm install` of `@wipcomputer/wip-ldm-os`. The current code deploys the built bridge to `~/.ldm/extensions/lesa-bridge/` but registers it as if it were a standalone install. The fix reads the parent's manifest field and registers with the bundled type instead.

## Acceptance

- Schema update: `bundled` updateSource type documented in `bin/ldm.js` source comments and the [parent design ticket](2026-05-13--cc-mini--installer-registry-source-types-architecture.md).
- Audit completed: a short document or section listing every currently-installed extension and confirming whether it's bundled or standalone. Audit results determine which other parents (beyond `wip-ldm-os-private` itself) land in this slice vs follow-up.
- `wip-ldm-os-private/package.json` declares `wipcomputer.bundledExtensions: ["lesa-bridge"]`.
- `lesa-bridge` registry entry uses `updateSource: { type: "bundled", ref: "@wipcomputer/wip-ldm-os" }` after a fresh `ldm install --alpha`.
- `ldm status` reports `lesa-bridge` row with "bundled" notation, no direct probe attempted.
- For any audit-confirmed bundled parents OUTSIDE `wip-ldm-os-private` (e.g., `wip-ai-devops-toolbox` sub-tools), either: (a) include those in this slice as a cross-repo PR, OR (b) file a follow-up ticket. Decision documented in the PR body. Do not silently expand this slice.
- Regression test: stage a fixture parent with `bundledExtensions` manifest + a bundled child; assert install reads the manifest and writes the correct registry entry; assert status doesn't probe for the bundled child; assert the row appears with the correct notation.
- Cycle detection: regression test stages parent A bundled in B, B bundled in A; assert registry error rather than infinite-loop.

## Why P2 not P1

P1 [Phase 1](2026-05-13--cc-mini--installer-source-npm-honest-cleanup.md) is the quick honest cleanup that moves rows into the `Untracked` section so nothing disappears. This Step 2 ticket is the architectural improvement that reclassifies `lesa-bridge` (and any other audit-confirmed bundled extensions) from `untracked` to `bundled` so they report **correctly** rather than just being labeled "pending."

## Out of scope

- `source.git` tracking — separate [Step 3 ticket](2026-05-13--cc-mini--installer-source-git.md).
- Heuristic detection of bundling without the manifest field. If a parent doesn't declare `wipcomputer.bundledExtensions`, its children get registered as standalone (whatever `ldm install` does today). The manifest is the contract.

## Recommendation

Alpha after fix. Dogfood `ldm status` and verify `lesa-bridge` reports as bundled.

## Related

- Parent: [Installer registry source types architecture](2026-05-13--cc-mini--installer-registry-source-types-architecture.md)
- Companion: [source.git support](2026-05-13--cc-mini--installer-source-git.md)
- Master ticket: [ldmos-bugs-masterticket--installer.md](ldmos-bugs-masterticket--installer.md)
