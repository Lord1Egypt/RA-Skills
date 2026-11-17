---
title: "Installer: ldm doctor registry hygiene audit (duplicates, phantoms, mystery entries)"
status: open
priority: P3
owner: Installer Cody
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-05-13
---

# Installer: `ldm doctor` registry hygiene audit

## Problem

Today's investigation of `~/.ldm/extensions/registry.json` found accumulated cruft from six-plus months of org renames, deprecations, and incomplete installs:

1. **Duplicate entries pointing at the same source:**
   - `cc-session-export` and `session-export` both claim `source.npm: "session-export"`. Same description, same version.
   - `wip-branch-guard` and `package` both claim `source.npm: "@wipcomputer/wip-branch-guard"`. Different versions (1.9.91 vs 1.9.90).

2. **Phantom entries (registry row, no directory on disk):**
   - `tavily` v1.0.2 with `source.npm: "@wipcomputer/openclaw-tavily"`. The directory `~/.ldm/extensions/tavily` does not exist. Likely a leftover from a rename to `openclaw-tavily`.

3. **Mystery entries (no source, no repo, no description):**
   - `run` v1.5.0 with `source: { npm: "no-npm", repo: "no-repo" }` and no description. Unknown provenance.

4. **Stale source references after deprecation:**
   - `lesa-bridge` declares `source.npm: "lesa-bridge"` but the repo `github.com/wipcomputer/wip-bridge-deprecated` was marked deprecated 2026-03-16 with the note "Bridge is now part of LDM OS (v0.3.0+)." The registry never caught up.

None of these break runtime. They accumulate as the org evolves and cause confusion every time the user reads `ldm status`.

## Proposal

Extend `ldm doctor` with a registry hygiene audit. Checks to add:

### Check 1: Duplicate source detection

For each `source.npm` value, count occurrences. If >1, list the duplicates:

```
warn: 2 registry entries share source.npm "session-export":
  - cc-session-export (v1.0.0)
  - session-export (v1.0.0)
  Action: confirm which is canonical and delete the other.
```

### Check 2: Phantom entry detection

For each registry entry, verify `~/.ldm/extensions/<name>/` exists on disk. If not:

```
warn: registry entry `tavily` v1.0.2 has no directory on disk.
  Action: rm-from-registry (the directory was probably renamed or deleted).
```

### Check 3: Mystery entry detection

For each registry entry, check whether `updateSource.type` is set (any of `npm`, `bundled`, `git`, `local`, `private`, `untracked`). If `updateSource` is empty or has no `type` AND `provenance` is empty AND no legacy `description`, mark as mystery:

```
warn: registry entry `run` v1.5.0 has no updateSource type, no provenance, no description.
  Action: investigate or delete.
```

### Check 4: Schema validator violations

For each registry entry, validate against the discriminator schema from the [parent design](2026-05-13--cc-mini--installer-registry-source-types-architecture.md):

- `updateSource.type` must be one of `npm`, `bundled`, `git`, `local`, `private`, `untracked`.
- For `type` in {`npm`, `bundled`, `git`, `local`}, `updateSource.ref` must be present (and a non-empty string).
- For `type` in {`private`, `untracked`}, `updateSource.ref` is optional.
- No extra fields beyond `type` and `ref` are permitted inside `updateSource`.
- `provenance` is optional. If present, must be an object (open shape; any string keys allowed).

```
warn: registry entry `<name>` has updateSource.type "git" but no updateSource.ref.
  Action: fix the entry, or run `ldm doctor --reclassify-sources`.
```

```
warn: registry entry `<name>` uses the legacy flat form `source.npm`. Migrate to discriminator form (updateSource + provenance).
  Action: run `ldm doctor --reclassify-sources`.
```

### Check 5: Deprecated-repo detection

For each entry with `updateSource.type: "git"`, check the GitHub repo's description for "DEPRECATED" prefix. If found:

```
warn: registry entry `<name>` tracks `wipcomputer/<repo>-deprecated` which is marked deprecated.
  Action: update updateSource.ref to the current canonical repo.
```

### Check 6: Stale untracked entries

For each registry entry with `updateSource.type: "untracked"`, check the `provenance.untrackedSince` timestamp (set when Phase 1 migrated the entry). If older than N days (suggest 30), warn:

```
warn: registry entry `<name>` has been `untracked` since 2026-05-13 (>30 days).
  Action: run `ldm doctor --reclassify-sources` to classify it, or set updateSource.type explicitly.
```

This catches entries that got migrated to `untracked` in Phase 1 but never reclassified, so they don't sit indefinitely.

(Note: the previous draft of this ticket had a "stale-source-npm" check. That check's job is now owned by Step 1's `ldm doctor` warning ([source-npm honest cleanup](2026-05-13--cc-mini--installer-source-npm-honest-cleanup.md)). The hygiene audit does not duplicate it.)

### Fix mode

Add `ldm doctor --fix-registry` that walks each warning and offers a per-entry action: skip, remove, edit. Non-destructive by default (no auto-deletes; prints what it would do). For source-type reclassification specifically, this command **defers** to `ldm doctor --reclassify-sources` ([migration ticket](2026-05-13--cc-mini--installer-source-types-migration.md)) rather than duplicating that logic.

## Acceptance

- `ldm doctor` runs Checks 1, 2, 3, 4, 5, 6 with no flags, printing warnings. (Stale-source-npm is intentionally NOT a check here; it lives in Phase 1.)
- `ldm doctor --fix-registry` is interactive (or with `--yes` for non-interactive), offering per-entry remediation. Source-type reclassification is delegated to `--reclassify-sources` rather than duplicated.
- Regression test: stage a fixture registry with one entry of each broken type (duplicate, phantom, mystery, schema-violation, deprecated-repo, stale-untracked). Assert each check fires.
- On Parker's mac-mini-01: running `ldm doctor` after this lands reports the duplicates, the `tavily` phantom, the `run` mystery, and any schema-validator violations or stale-untracked entries remaining from the migration.

## Why P3

The runtime works fine without this. It's a debt-reduction tool, not a fix for a current failure. Best done after the source-types architecture lands so the audit can distinguish "wrong source" from "no source specified yet."

## Out of scope

- Auto-detecting deprecated repos via GitHub description scrape if the repo has `source.npm` only (no `source.git`). The deprecation note is on the repo, and the repo isn't known until git tracking lands.
- Auto-fixing the bare-name PRIVATE convention violations (`wip-root-key`, `openclaw-tavily`, etc.). That's a `wip-repos` concern, not installer.

## Recommendation

No release on its own. Ships in the same alpha as one of the source-types steps when convenient. Pure tooling addition.

## Related

- Parent: [Installer registry source types architecture](2026-05-13--cc-mini--installer-registry-source-types-architecture.md)
- Master ticket: [ldmos-bugs-masterticket--installer.md](ldmos-bugs-masterticket--installer.md)
