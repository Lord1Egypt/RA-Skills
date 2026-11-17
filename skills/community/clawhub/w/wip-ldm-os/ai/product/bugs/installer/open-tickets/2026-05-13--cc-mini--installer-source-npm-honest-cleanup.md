---
title: "Installer: source.npm honest cleanup (Step 1 of source-types refactor)"
status: open
priority: P1
owner: Installer Cody
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-05-13
---

# Installer: `source.npm` honest cleanup

## Problem

`~/.ldm/extensions/registry.json` currently has 10 entries where `source.npm` points at an npm package name that returns 404 from the public npm registry. `ldm status` probes those names anyway, gets 404, and reports the rows as `[unavailable]`. This is a euphemism for "I tried to check but the package doesn't exist."

The rows shouldn't be probed in the first place if we know the npm package doesn't exist.

## Affected entries (from 2026-05-13 dogfood)

| Registry name | `source.npm` claim | Actual npm state |
|---|---|---|
| `cc-session-export` | `session-export` | 404 |
| `session-export` | `session-export` | 404 (duplicate of above) |
| `compaction-indicator` | `compaction-indicator` | 404 |
| `context-embeddings` | `@openclaw/context-embeddings` | 404 (scope inactive) |
| `lesa-bridge` | `lesa-bridge` | 404 (bundled in `@wipcomputer/wip-ldm-os` since v0.3.0) |
| `root-key` | `root-key` | 404 |
| `tavily` | `@wipcomputer/openclaw-tavily` | 404 (and directory missing) |
| `wip-agent-pay` | `wip-agent-pay` | 404 |
| `openclaw-tavily` | `@wipcomputer/openclaw-tavily` | 404 (your fork; public `openclaw-tavily@0.2.1` exists unscoped) |
| `package` | `@wipcomputer/wip-branch-guard` | exists (duplicate of `wip-branch-guard` row) |

Some are bundled (`lesa-bridge`), some are git-only (most), some are forks (`openclaw-tavily`), some are duplicates. This ticket is the **quick honest fix**: remove `source.npm` from entries where the probe is known-bad. The proper homes (bundled, git, private, fork) come in sibling tickets ([source.bundled](2026-05-13--cc-mini--installer-source-bundled.md), [source.git](2026-05-13--cc-mini--installer-source-git.md)).

## Proposed fix

Three-step approach. **The acceptance rule is: real installed-extension inventory is conserved. Phantom and duplicate removals are reported separately and explicitly.** Rows for the actually-installed extensions still appear in `ldm status`, just labeled honestly. The bad probes stop.

### Step A: One-time registry pass (migrate; preserve legacy fields in provenance)

For each entry whose `source.npm` returns 404 from npm registry AND has a real on-disk directory, migrate the entry as follows:

```jsonc
"<name>": {
  "updateSource": { "type": "untracked" },
  "provenance": {
    "legacy-npm-name": "<the original source.npm value>",   // preserved for migration
    "repo": "<the original source.repo value, if present>", // preserved for migration
    "untrackedSince": "<ISO 8601 timestamp>"                 // for hygiene-audit staleness
  },
  "installed": { ... }   // unchanged
}
```

Do NOT delete the entry. Do NOT silently discard the legacy `source.npm` or `source.repo` values; carry them into `provenance` so the migration command (Phase 2) and the hygiene audit (Phase 2/3) can read them. The `untracked` type is a transitional classification (per the [parent design](2026-05-13--cc-mini--installer-registry-source-types-architecture.md)) that says "this extension is installed, but we haven't classified its source yet." It does not attempt any probe.

Exception: phantom entries (registry row with no on-disk directory; the `tavily` case) ARE removed. The directory is gone; nothing to track. **Phantom removals are reported in a separate post-cleanup summary line** so the inventory delta is visible: e.g., "Removed 1 phantom entry (tavily; directory missing)."

Exception: duplicate entries (`cc-session-export` + `session-export`, `wip-branch-guard` + `package`) are deduped to one canonical entry each. **Dedupe removals are reported in a separate post-cleanup summary line** so the inventory delta is visible: e.g., "Removed 2 duplicate entries (session-export merged into cc-session-export; package merged into wip-branch-guard)."

### Step B: `ldm status` shows an Untracked section

`ldm status` output is extended to include a new section for `untracked` entries:

```
Untracked extensions (pending reclassification):
  cc-session-export      v1.0.0
  compaction-indicator   v1.0.1
  context-embeddings     v0.2.0
  lesa-bridge            v0.3.0
  root-key               v0.2.0
  wip-agent-pay          v1.0.0
  openclaw-tavily        v1.0.1
  ...
  (run `ldm doctor --reclassify-sources` to classify these)
```

Real installed-extension inventory is conserved (every entry with an on-disk directory still appears in `ldm status` after the cleanup). The `[unavailable]` rows disappear; the same rows reappear in the new Untracked section with a clear next-step action. Phantoms and dedupes are explicit deltas reported separately, not silent disappearances. No UX whiplash when Phase 2's status-output reformat lands.

### Step C: `ldm doctor` detection

Add a check to `ldm doctor` that warns when a registry entry has `source.npm: "<name>"` (legacy form) or `updateSource.type: "npm"` with `ref: "<name>"` (discriminator form) and a `fetch` to the npm registry returns 404. Prints a line like:

```
warn: extension `lesa-bridge` declares an npm source for "lesa-bridge" but the package does not exist on npm. Run `ldm doctor --reclassify-sources` to migrate it to the correct type, or update the registry manually.
```

This catches future drift when someone deprecates a package without updating the registry. The reclassification itself lives in the [source-types migration ticket](2026-05-13--cc-mini--installer-source-types-migration.md).

## Acceptance

- For each entry whose legacy `source.npm` returns 404 (and that has a real on-disk directory), the entry is migrated to `updateSource: { type: "untracked" }`. The entry is NOT deleted.
- When migrating an entry to `untracked`, the legacy `source.npm` value is preserved as `provenance.legacy-npm-name`, the legacy `source.repo` value (if present) is preserved as `provenance.repo`, and `provenance.untrackedSince` is set to the migration timestamp (ISO 8601). These fields are load-bearing for downstream tickets ([migration rules 7-8](2026-05-13--cc-mini--installer-source-types-migration.md) and [hygiene audit Check 6](2026-05-13--cc-mini--installer-registry-hygiene-audit.md)).
- Phantom `tavily` entry (registry row with no on-disk directory) is removed entirely. Removal is reported in a post-cleanup summary line (e.g., "Removed 1 phantom entry").
- Duplicate entries (`cc-session-export` vs `session-export`, `wip-branch-guard` vs `package`) are deduped: one canonical entry per actual extension. Removals are reported in a post-cleanup summary line.
- **Real installed-extension inventory is conserved.** Every entry with an on-disk directory and not a duplicate continues to appear in `ldm status`. Phantom/dedupe deltas are visible as explicit summary lines, not as silent row count changes.
- `ldm status` output shows an `Untracked extensions` section listing every `untracked` entry.
- Zero false npm probes attempted (network calls to registry.npmjs.org for entries marked `untracked` should be zero).
- `ldm doctor` reports a warning for any registry entry whose npm name 404s and gives a remediation pointer.
- Mystery entry `run` (no source, no repo, no description) is either migrated to `untracked` (so it still appears) or removed if Parker confirms it's debris; the choice is recorded in the post-cleanup summary.

## Why this is P1

The unavailable rows are eroding trust in `ldm status` reporting. Parker's exact words today: "I have to stop everything now because this is bad, this is really bad. I don't even know how much is broken." The reality is nothing is broken at runtime, but the report makes it look broken. P1 because the trust-restoration value is high and the work is small.

## Out of scope

- Classifying entries into correct new types (`bundled`, `git`, `private`) — that's the [migration ticket](2026-05-13--cc-mini--installer-source-types-migration.md). This Step 1 only removes wrong fields; classification is its own slice.
- Migrating bundled entries to `bundled` type — that's the [source.bundled ticket](2026-05-13--cc-mini--installer-source-bundled.md).
- Migrating git-only entries to `git` type — that's the [source.git ticket](2026-05-13--cc-mini--installer-source-git.md).
- New schema fields — this ticket only removes wrong fields, doesn't add new ones.

## Recommendation

After fix lands: cut alpha. Dogfood `ldm status` and verify the unavailable count drops to 0 (or matches genuinely-no-source entries).

## Related

- Parent: [Installer registry source types architecture](2026-05-13--cc-mini--installer-registry-source-types-architecture.md)
- Master ticket: [ldmos-bugs-masterticket--installer.md](ldmos-bugs-masterticket--installer.md)
