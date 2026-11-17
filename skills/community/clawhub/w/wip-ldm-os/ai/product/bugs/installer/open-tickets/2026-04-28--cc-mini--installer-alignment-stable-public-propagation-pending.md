# Universal Installer alignment: stable/public propagation pending toolbox stable promotion

**Date:** 2026-04-28
**Owner:** unassigned
**Status:** open
**Master plan:** [2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md](2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md)

## What

The universal-installer skill/docs alignment landed on `wip-ai-devops-toolbox-private` main (PR #396 → merge `053ae4d`) and was released as alpha cut `v1.9.73-alpha.6` (2026-04-28). It is **not yet on the public mirror** (`wipcomputer/wip-ai-devops-toolbox`) because the toolbox is mid-alpha and `deploy-public` does not run during alpha cuts (alpha is dev-only by policy).

Stable/public propagation is pending the next intentional toolbox stable promotion. That promotion is a separate decision because it would also stabilize five other alpha cuts (1.9.73-alpha.1 through alpha.6) including wip-release fixes, branch-guard changes, the SKILL.md publish-on-prerelease gap fix, the installer-alignment skill refresh, and others. We did not promote-to-stable as part of the docs PR per Parker's explicit instruction: "don't accidentally turn five alpha cuts into stable just to publish this docs change."

## Blocker discovered during the alpha publish (must resolve before stable promotion)

`@wipcomputer/universal-installer` failed to publish during the 1.9.73-alpha.6 cut:

```
npm error Cannot implicitly apply the "latest" tag because previously published version 2.1.5 is higher
than the new version 1.9.69. You must specify a tag using --tag.
```

Root cause: the sub-tool's `package.json` is at `1.9.69` (toolbox-coordinated), but a prior manual publish put `2.1.5` on npm under the `latest` tag. wip-release's implicit-latest publish is refused by npm because it would be a downgrade.

Three other sub-tools (wip-license-hook, wip-readme-format, wip-repo-permissions-hook) published cleanly at 1.9.69. The root toolbox published at 1.9.73-alpha.6 with the `alpha` dist-tag.

This means the canonical docs change *is* in the published artifact contents (root toolbox tarball includes everything via deploy-public eventually), but the `@wipcomputer/universal-installer` sub-tool npm package itself is frozen at 2.1.5 until the version drift is resolved.

## What needs to happen before stable promotion

1. **Decide the canonical version line for `@wipcomputer/universal-installer`.** ✅ **DECIDED 2026-04-29: Option A (preserve 2.x line, bump source to 2.2.0).**
   - Option A: bump the sub-tool's `package.json` past `2.1.5` (e.g. `2.1.6`) so npm accepts the publish. **← chosen, see "Decision recorded" below.**
   - Option B: deprecate `@wipcomputer/universal-installer@2.1.5` from npm and continue the toolbox-coordinated 1.9.x line. *Rejected: treats npm history as not canonical.*
   - Option C: switch the sub-tool to a fully independent release cadence (its own license-guard, its own version) and stop trying to publish it via root cuts. *Rejected: too speculative for a docs-driven version skew; revisit only if the alpha-train coordination keeps misbehaving.*
2. **Decide whether/when to promote `1.9.73-alpha.6 → 1.9.73` stable.** This stabilizes the alpha train and triggers `deploy-public` for the universal-installer alignment. *Still open; explicitly out of scope for the version-skew fix per Parker's "do not promote the alpha train" instruction.*
3. **Verify after promotion:** docs at `https://github.com/wipcomputer/wip-ai-devops-toolbox/tree/main/tools/wip-universal-installer/` reflect the eight-interface model + AGENTS.md note + LSP future-consideration + disposable-artifacts cross-ref.

## Decision recorded ... 2026-04-29: Option A, bump to 2.2.0

**Decision:** preserve the existing npm 2.x line. Treat npm history as canonical. Bump the source `tools/wip-universal-installer/package.json` from `1.9.68` to `2.2.0` (minor, not patch).

**Why 2.2.0 vs 2.1.6:** npm 2.1.5's published description listed only six interfaces (CLI, Module, MCP Server, OpenClaw Plugin, Skill, Claude Code Hook). The toolbox sub-tool source now describes eight interfaces in canonical order with Remote MCP at #4 and Claude Code Plugin at #8 (landed in PR #396). Adding two interfaces to the published taxonomy is "added functionality, backwards compatible" → minor.

**Also restored in the same PR (drift the sub-tool dropped vs npm 2.1.5):**
- `bin: { "wip-install": "install.js" }` ... the standalone CLI `install.js` exists, SKILL.md still documents `wip-install` as the fallback CLI, every other sub-tool (wip-license-hook, wip-readme-format) declares `bin`. The drop in the sub-tool's package.json was unintentional.
- `exports./install` ... parity with 2.1.5 so consumers that import the installer programmatically don't break.

**Refreshed metadata:**
- `description`: now names all eight interfaces.
- `repository`: switched from old standalone `wip-universal-installer` repo URL to `wipcomputer/wip-ai-devops-toolbox` with `directory: tools/wip-universal-installer` (npm monorepo sub-package convention).
- `homepage`: points at the toolbox sub-tool directory (the README cross-links to the canonical SPEC at `wipcomputer/wip-ldm-os`).
- `keywords`: added `remote-mcp`, `claude-code-plugin`.

**Validated:** `npm publish --dry-run --access public` from `tools/wip-universal-installer/` returns `+ @wipcomputer/universal-installer@2.2.0` with no skew error.

**Tracked in:** wip-ai-devops-toolbox-private PR `#403` ([fix(wip-universal-installer): bump to 2.2.0, resolve npm version skew, restore wip-install bin](https://github.com/wipcomputer/wip-ai-devops-toolbox-private/pull/403)). Done in a fresh worktree off `origin/main` to avoid contaminating with the dirty +1 sub-tool bumps sitting in the shared toolbox main checkout (likely in-flight state from a parallel session preparing alpha.9, treated as contested per Parker's instruction).

**Still pending (separate decisions):**
- Release path: whether `@wipcomputer/universal-installer@2.2.0` ships as a sub-tool-only cut or rides the next toolbox alpha/stable train. Investigate after PR #403 merges.
- Stable promotion of the alpha train.
- Public mirror sync for the universal-installer alignment.

## Verification commands (for the eventual promotion)

```bash
# After stable promote + deploy-public:
gh release view --repo wipcomputer/wip-ai-devops-toolbox --json tagName,name,url
curl -s https://raw.githubusercontent.com/wipcomputer/wip-ai-devops-toolbox/main/tools/wip-universal-installer/SKILL.md | grep -E "Eight Universal Interfaces|AGENTS.md|disposable, agent-generated"
npm dist-tag ls @wipcomputer/wip-ai-devops-toolbox  # latest should equal stable promote
npm dist-tag ls @wipcomputer/universal-installer    # latest should be > 2.1.5 OR explicitly retagged
```

## Acceptance

- Sub-tool npm version drift resolved (decision recorded above).
- Toolbox stabilized when the alpha train is intentionally cut (separate decision, not blocked by this ticket).
- Public mirror reflects the universal-installer alignment.
- Master plan ticket links here so future readers see why public lagged private.

## Context

- Private alpha release: `v1.9.73-alpha.6` (2026-04-28)
- Sibling release that DID propagate to public: `@wipcomputer/wip-ldm-os@0.4.84` (2026-04-28). The canonical docs at `wip-ldm-os/docs/universal-installer/` are live on the public mirror; only the toolbox tool docs are pending.

## Operational caution (added 2026-05-01)

Before the next toolbox root alpha cut, **the release owner must pull/rebase onto main after PR #403 (`274c969`)** so `tools/wip-universal-installer/package.json` is `2.2.0`. A stale dirty checkout with the old `1.9.69` bump will hit the same npm downgrade refusal we already documented above (npm `latest` is `2.1.5`; `1.9.69 → 2.1.5` is a downgrade and npm refuses).

Verify before running `wip-release`:

```bash
cd /Users/lesa/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private
git status                    # must be clean (no dirty package.json bumps)
git log -1 tools/wip-universal-installer/package.json --pretty=oneline   # must show 274c969 or newer
node -p "require('./tools/wip-universal-installer/package.json').version"  # must print 2.2.0
```

If `git status` is dirty with stale `1.9.69` bumps from a prior in-flight session, **stash or discard them only after confirming they don't belong to another active session**. Per the original 2026-04-29 dirty-state observation: those bumps may belong to whoever was preparing the alpha cut you're about to run; coordinate before destroying.
