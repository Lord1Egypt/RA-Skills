---
title: "Installer: source-types migration via ldm doctor --reclassify-sources"
status: open
priority: P2
owner: Installer Cody
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-05-13
---

# Installer: source-types migration

## Problem

The source-types refactor splits `updateSource` (exclusive discriminator: npm/bundled/git/local/private/untracked) from `provenance` (free-form optional metadata). Existing registry entries on real machines today use the legacy flat form `source: { npm: "<name>" }`. Phase 1 migrates obviously-bad entries to `updateSource.type: "untracked"` so nothing disappears. Sub-tickets [Step 1 honest cleanup](2026-05-13--cc-mini--installer-source-npm-honest-cleanup.md), [Step 2 bundled](2026-05-13--cc-mini--installer-source-bundled.md), and [Step 3 git](2026-05-13--cc-mini--installer-source-git.md) each touch the schema but none of them owns the **classification decision**: for any given untracked entry, which final `updateSource.type` does it become, and what `provenance` should be populated?

Without a named migration command, every existing entry needs hand-classification. That's brittle, slow, and prone to drift between machines.

## Proposal

One canonical command: `ldm doctor --reclassify-sources`.

### Inputs

The current `~/.ldm/extensions/registry.json` (each entry, regardless of legacy or new form).

### Per-entry classification rules

For each registry entry, in this order (first match wins). For each match, the command writes BOTH `updateSource` (the discriminator decision) AND, where applicable, `provenance` (free-form historical metadata).

1. **Already-migrated:** entry already has `updateSource.type` set to a non-untracked value. Skip; report "ok".
2. **Phantom:** `~/.ldm/extensions/<name>/` does not exist on disk. Propose deletion. Report "phantom".
3. **Duplicate:** another entry has the same `source.npm` (or `updateSource.ref` if migrated) value AND the same description AND the same installed version. Propose deletion of duplicate. Report "duplicate".
4. **Bundled candidate:** the parent package's `package.json` declares this entry name in `wipcomputer.bundledExtensions` (per Step 2's manifest contract). Propose `updateSource: { type: "bundled", ref: "<parent>" }` plus `provenance: { ... }` carrying any legacy `repo` field for human reference. Report "bundled candidate".
5. **Git candidate:** the legacy `source.repo` field is present and reasonable (matches `^[\w-]+/[\w.-]+$`) and `gh api repos/<repo>` returns 200. Propose `updateSource: { type: "git", ref: "<owner>/<repo>" }`. If the legacy entry had `source.npm` that 404s AND this git repo's name suggests a fork-of-public-package, propose `provenance: { "fork-of": "<upstream-name>" }`. Report "git candidate".
6. **NPM-current:** `source.npm` is present and `fetch` to `https://registry.npmjs.org/<name>` returns 200. Migrate to `updateSource: { type: "npm", ref: "<name>" }`. Carry the legacy `repo` field as `provenance.repo` if present. Report "npm migrated".
7. **NPM-404 fallthrough:** `source.npm` returns 404, no `source.repo`, no known bundled parent. Propose `updateSource: { type: "private" }` plus `provenance: { "legacy-npm-name": "<the 404 name>" }` so the original claim isn't lost. Report "private (defaulted)".
8. **Untracked carry-over:** entry has `updateSource.type: "untracked"` from Phase 1. Re-run rules 4-7 on its legacy fields. Whichever rule matches first wins. Report whichever rule fired.
9. **No source / mystery:** entry has no `source.npm`, no `source.repo`, no recognizable info, no `provenance`. Propose deletion OR `updateSource: { type: "private" }` per user choice. Report "mystery".

### Modes

- **Default (no flag):** interactive. For each non-trivial proposal (anything but "ok" and "npm migrated"), print the proposed change and prompt yes/no/skip.
- **`--yes`:** auto-apply all proposals. Skip prompts. Best for fresh-install machines where the registry is small.
- **`--dry-run`:** show all proposals, change nothing.
- **`--json`:** machine-readable proposal list.

### Output

Per-entry report:

```
ok           wip-release            (already migrated)
npm migrated wip-repos              source.npm "@wipcomputer/wip-repos" -> { type: "npm", ref: "@wipcomputer/wip-repos" }
bundled      lesa-bridge            -> { type: "bundled", ref: "@wipcomputer/wip-ldm-os" }   [APPLY? y/n/s]
git          root-key               -> { type: "git", ref: "wipcomputer/wip-root-key" }       [APPLY? y/n/s]
private      compaction-indicator   no source detected, defaulting to private                 [APPLY? y/n/s]
duplicate    session-export         duplicate of `cc-session-export`, propose deletion        [APPLY? y/n/s]
phantom      tavily                 directory missing, propose deletion                       [APPLY? y/n/s]
mystery      run                    no source, no repo, no description                        [APPLY? y/n/s]
```

### Non-destructive guarantee

Default mode never writes to the registry without explicit per-entry confirmation. Even `--yes` mode never deletes a registry entry whose `~/.ldm/extensions/<name>/` directory still exists on disk; deletion proposals require the user to confirm a `.bak` is written first.

### Bundled-children manifest contract

The bundled-candidate rule (rule 4) reads the parent package's `wipcomputer.bundledExtensions` manifest field (per [Step 2](2026-05-13--cc-mini--installer-source-bundled.md)). If no parent declares the entry, the rule does not fire — better to leave it for one of the later rules than to invent a bundled parent.

## Acceptance

- `ldm doctor --reclassify-sources` runs all 9 classification rules in order.
- Interactive mode prompts per-entry for non-trivial proposals; `--yes` and `--dry-run` modes work.
- All proposals are non-destructive in default mode.
- For each successful classification, the command writes BOTH `updateSource` AND, where applicable, `provenance`. Legacy fields like `source.repo` and the original `source.npm` value are not silently discarded; they become `provenance` entries.
- Regression test: stage a fixture registry containing one entry of each classification (phantom, duplicate, bundled, git, npm-current, npm-404 → private, untracked carry-over, mystery) and assert each reaches the correct rule. Assert provenance is populated correctly for each.
- On Parker's mac-mini-01: running `ldm doctor --reclassify-sources --dry-run` after this lands produces the expected proposals for the `untracked` entries left by Phase 1 (5 bundled, ~4 git-candidate / private-defaulted, 1 duplicate, 1 phantom — actual numbers depend on what Phase 1 leaves behind).
- `--reclassify-sources` is the only documented migration command. Any earlier references (`--fix-source-types`, `--fix-registry`) in other tickets are renamed to point here.

## Why P2

Phase 1's [npm honest cleanup](2026-05-13--cc-mini--installer-source-npm-honest-cleanup.md) ships first and removes wrong fields, but doesn't classify entries into the right new types. That classification work has to happen for the new schema to be useful, but it can land in Phase 2 alongside the `source.bundled` and `source.git` work. Without migration, Steps 2 and 3's schema changes have no real-world entries to dispatch on.

## Out of scope

- Migrating `source.local` entries (`source.local` is descoped this iteration per the parent design's Out of Scope).
- Cross-machine sync of registry state. Each machine runs its own `--reclassify-sources` interactively.
- Automatic re-classification when an upstream extension's source moves (e.g., npm package is unpublished and the repo becomes the canonical source). Filed as a future enhancement only if the drift becomes common.

## Recommendation

Alpha after fix. Lands together with Step 2 or Step 3 (whichever ships first), since the schema and migration are co-dependent for any user-visible benefit.

## Related

- Parent: [Installer registry source types architecture](2026-05-13--cc-mini--installer-registry-source-types-architecture.md)
- Companion: [Step 1 honest cleanup](2026-05-13--cc-mini--installer-source-npm-honest-cleanup.md), [Step 2 bundled](2026-05-13--cc-mini--installer-source-bundled.md), [Step 3 git](2026-05-13--cc-mini--installer-source-git.md)
- Master ticket: [ldmos-bugs-masterticket--installer.md](ldmos-bugs-masterticket--installer.md)
