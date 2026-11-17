---
title: "Installer architecture: registry source types (design parent)"
status: open
priority: P1
owner: Installer Cody
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-05-13
---

# Installer architecture: registry source types

## Problem

`~/.ldm/extensions/registry.json` tracks every installed extension with a single source field, effectively `source: { npm: "<package-name>" }`. When `ldm status` checks for updates, it probes public npm for that package name. If the package doesn't exist on public npm, the row is reported as `unavailable`. That's a euphemism for "the installer doesn't know how to check this."

Today's dogfood (2026-05-13) showed 10 of 32 installed extensions report as unavailable. Breakdown of why:

- **5 bundled extensions** that ship inside parent npm packages and are not standalone npm packages themselves (e.g., `lesa-bridge` ships inside `@wipcomputer/wip-ldm-os` since v0.3.0, per the deprecation note in `github.com/wipcomputer/wip-bridge-deprecated`).
- **4 git-only extensions** that have private GitHub repos but were never published to npm (`compaction-indicator`, `root-key`, `wip-agent-pay`, `dream-weaver-protocol`).
- **1 fork** that lives only locally (`openclaw-tavily@1.0.1`, ahead of the public `openclaw-tavily@0.2.1`).

The installer can't honestly report on any of these because the registry only knows one source type.

## Vision

The installer should know **where each extension comes from** and **how to check it for updates**, independent of npm. The end-user model:

> Install anything (npm, git, local, bundled). The installer tracks what's installed, knows where it came from, and tells you if there's an update available, from the right source.

## Proposed schema

The previous draft of this ticket conflated **update source** (which drives the probe) with **provenance** (where the extension came from). The Codex reviewer correctly noted these are different: a bundled extension can legitimately have an upstream repo for human reference; a fork is `git` for updates AND has an upstream-derived origin. Splitting them is cleaner.

Two fields in the registry entry:

### `updateSource` (exclusive, drives probes)

```jsonc
{ "updateSource": { "type": "npm",     "ref": "@wipcomputer/wip-release" } }        // probe public npm
{ "updateSource": { "type": "bundled", "ref": "@wipcomputer/wip-ldm-os" } }         // updates ride with parent
{ "updateSource": { "type": "git",     "ref": "wipcomputer/wip-root-key" } }        // probe GitHub releases/tags
{ "updateSource": { "type": "local",   "ref": "/Users/lesa/wipcomputerinc/..." } }  // local dev path (descoped this iteration)
{ "updateSource": { "type": "private" } }                                            // user-controlled opt-out
{ "updateSource": { "type": "untracked" } }                                          // legacy entry awaiting reclassification (see Phase 1)
```

Exactly one `type` per entry. `ref` is required for all types except `private` and `untracked`. A validator enforces this at registry write time and as part of [Step 6 registry hygiene audit](2026-05-13--cc-mini--installer-registry-hygiene-audit.md).

The `untracked` value is a transitional state: Phase 1's honest cleanup marks legacy bad-`source.npm` entries as `untracked` instead of deleting their source field, so they still appear in `ldm status` (in a dedicated "Untracked" section) until the [migration ticket](2026-05-13--cc-mini--installer-source-types-migration.md) reclassifies them properly. No inventory hidden.

### `provenance` (optional, free-form, can have multiple fields)

```jsonc
{ "provenance": {
    "repo": "wipcomputer/wip-bridge-deprecated",     // historical repo reference
    "fork-of": "openclaw-tavily",                    // for forks: name of upstream package
    "upstream-version-at-fork": "0.2.1",             // semver of upstream when forked
    "notes": "Bridge code moved into wip-ldm-os v0.3.0; original repo deprecated 2026-03-16."
} }
```

Fields are optional. Schema is open (any string keys allowed). Provenance does NOT drive probes; it exists for humans and agents to read.

**Forks:** `updateSource.type: "git"` pointing at the local fork's git repo, plus `provenance.fork-of` naming the upstream package. `ldm status` reports `local v1.0.1 vs upstream v0.2.1` cases as "ahead of upstream" when `semverNewer(local, upstream)` is true; not flagged as an update available. No new fork type needed.

**`private` semantics (clarification):** `updateSource.type: "private"` is a **user-controlled opt-out**, not a claim about the repo's GitHub visibility. An agent or the user can mark any entry as private to suppress its probe. Org-internal/closed-source repo visibility is a separate concern (a `wip-repos` concern, not installer). Examples of legitimate `private` use: a personal experiment the user doesn't want auto-checked; a deprecated extension kept for posterity; an extension whose source moved and the user hasn't reclassified yet.

## How `ldm status` dispatches per `updateSource.type`

| `type` | Probe action | Update detection |
|---|---|---|
| `npm` | `fetch` to registry.npmjs.org (current alpha.27 behavior) | Compare `dist-tags.latest` to installed version |
| `bundled` | Skip direct probe | "Updates via parent <ref>" line; parent's update detection covers it |
| `git` | `gh api repos/<ref>/releases/latest` (or `/tags`) | Compare newest tag to installed version. If local > upstream, report "ahead of upstream" (fork case). |
| `local` | (descoped this iteration; see Out of scope) | (n/a) |
| `private` | Skip cleanly | "Auto-check disabled" line; no probe attempted |
| `untracked` | Skip cleanly | "Pending reclassification" line; transitional state from Phase 1 |

Result: zero false-probe `unavailable` rows. Every row reports a real status from the right source, including transitional rows that say so explicitly.

## Acceptance (design level)

- Schema documented in this ticket and in `bin/ldm.js` source comments. `updateSource` (exclusive discriminator) and `provenance` (optional, open) are both normative.
- Schema validator at registry write time rejects entries that have unknown `updateSource.type`, missing `ref` (for types that need one), or invalid `updateSource` shape. `provenance` is permissive (any keys allowed; the validator just confirms it's an object if present).
- **`updateSource.type: "local"` is on the validator deny-list this iteration.** The type remains reserved in the schema for forward compatibility (so a future ticket can re-admit it without a schema rev), but no registry entry may be written with `type: "local"` until local-path tracking has implementation backing. Rationale: today there is no probe code or row treatment for `local`, so admitting it would create a contradiction with downstream tickets' "every entry produces exactly one row" promise. When local-path tracking ships, this acceptance bullet gets updated to re-admit the type.
- Migration path: existing registry entries (legacy flat `source.npm` form) are reclassified into the new shape by `ldm doctor --reclassify-sources` (see [migration ticket](2026-05-13--cc-mini--installer-source-types-migration.md)).
- Implementation split into the sub-tickets below (one slice per accepted type, plus one migration slice).

## Sub-tickets (work order)

1. **Phase 1 honest cleanup** ([2026-05-13--cc-mini--installer-source-npm-honest-cleanup.md](2026-05-13--cc-mini--installer-source-npm-honest-cleanup.md)) ... P1. Migrates legacy bad-`source.npm` entries to `updateSource: { type: "untracked" }` so they still appear in `ldm status` but with a non-misleading label and zero false npm probes. Also introduces the `Untracked` section in `ldm status` output. Same row count before and after. Inventory is never hidden.
2. **Migration: reclassify untracked entries** ([2026-05-13--cc-mini--installer-source-types-migration.md](2026-05-13--cc-mini--installer-source-types-migration.md)) ... P2. One canonical `ldm doctor --reclassify-sources` command that walks the registry, infers correct `updateSource.type`/`ref` and populates `provenance` where applicable, and proposes per-entry remediation. Non-destructive default; `--yes` for batch apply.
3. **`bundled` updateSource type** ([2026-05-13--cc-mini--installer-source-bundled.md](2026-05-13--cc-mini--installer-source-bundled.md)) ... P2. Add the type + dispatch, wire into status output, mark `lesa-bridge` first. Cross-repo work on `wip-ai-devops-toolbox` is gated by an audit (see ticket); it doesn't automatically expand scope.
4. **`git` updateSource type** ([2026-05-13--cc-mini--installer-source-git.md](2026-05-13--cc-mini--installer-source-git.md)) ... P2. The big one. Adds GitHub release/tag tracking via `gh api` **inside the installer only**. Agents in the install flow continue calling `ldm status` / `ldm install --dry-run` — the `gh api` dispatch is not a sanctioned end-run around the install-prompt policy.
5. **`ldm status` output reformat** ([2026-05-13--cc-mini--installer-status-show-all-extensions.md](2026-05-13--cc-mini--installer-status-show-all-extensions.md)) ... P2. Source-type categorization. Folds `source.local` and `source.private` minimal implementations in here (since `local` is descoped and `private` only needs a categorization section). Stop silently dropping rows.
6. **Registry hygiene audit** ([2026-05-13--cc-mini--installer-registry-hygiene-audit.md](2026-05-13--cc-mini--installer-registry-hygiene-audit.md)) ... P3. `ldm doctor` detects duplicates, phantoms, mystery entries, schema-validator violations, and stale `untracked` entries (any entry that's been `untracked` for >N days could be flagged for follow-up).

## Why this is P1

The current dogfood-validated behavior (alpha.27) is technically correct but reports a misleading picture: it claims it tried to check 10 extensions and couldn't, when in reality it doesn't know how to check them and the registry never told it. Trust in `ldm status` requires accurate reporting. Trust in the installer requires understanding what it actually tracks.

This is the foundation work for everything else in the installer queue. Most of the older bugs in this folder (extension-docs generation, plugin install behaviors, eight-interfaces work) assume a single source path. Fixing the source-types architecture first means those subsequent fixes don't get re-built on a stale assumption.

## Out of scope

- Authentication for private GitHub repos beyond what `gh` CLI already provides. Use `gh` exclusively.
- Caching of registry probe results across `ldm status` invocations. Separate concern (perf, not correctness).
- Auto-publishing to npm. The schema describes what's tracked; it doesn't change publish policy.
- Repo naming convention enforcement (which is a `wip-repos` concern, not installer).
- **`updateSource.type: "local"` implementation.** Reserved in the schema for future development-mode work. This iteration ships the type but does not implement local-path tracking or `git status` integration. Any local-installed extension uses `type: "private"` for now to suppress probing.
- Agent-facing `gh` access during the install flow. The install-prompt policy (alpha.25) forbids agents from running raw `gh release` or `gh api` during install-state detection. This design uses `gh api` **inside the installer** (in `cmdStatus`) only. Agents continue to call `ldm status` and `ldm install --dry-run` and let the installer handle the `gh` dispatch internally. The presence of `gh api` here does not unlock a sanctioned agent end-run.

## Recommendation

No release for this design ticket alone. The implementation lands in the sub-tickets. Each sub-ticket cuts its own alpha after merge.

## Related

- Master ticket: [ldmos-bugs-masterticket--installer.md](ldmos-bugs-masterticket--installer.md)
- Triggered by: 2026-05-13 dogfood after alpha.27 shipped (clean install-prompt UX but revealed registry drift)
- Supersedes the silent-drop behavior in `cmdStatus` that pre-dates alpha.27.
