---
title: "Installer: ldm status must show ALL installed extensions categorized by source type"
status: open
priority: P2
owner: Installer Cody
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-05-13
---

# `ldm status` must show all installed extensions, categorized by source type

## Problem

The agent-built summary tables in today's dogfoods kept showing fewer rows than the registry contained:

- 2026-05-12 dogfood: agent's table had 17 rows; registry had 32 extensions. 15 entries silently dropped.
- 2026-05-13 dogfood: `ldm status` itself was honest about the skipped 10, but the agent's response still chose what to surface.

The current code path in `cmdStatus` (after alpha.27) writes three sections:

```
Update summary: <N> extension update(s) available, <M> update check(s) skipped
Updates available: [rows]
Update checks skipped: [rows]
```

Two problems with the current shape:

1. **Extensions with `source: { npm: "no-npm" }` (intentional opt-out) don't appear at all.** They're just dropped from the loop. The user has no idea those extensions are installed.
2. **The "skipped" section conflates several different things** under one `[unavailable Xms]` label: 404 from npm, network failure, timeout, deliberately-no-npm. They look the same to the reader.

After the source-types refactor ([parent design](2026-05-13--cc-mini--installer-registry-source-types-architecture.md), [Step 1](2026-05-13--cc-mini--installer-source-npm-honest-cleanup.md), [Step 2 bundled](2026-05-13--cc-mini--installer-source-bundled.md), [Step 3 git](2026-05-13--cc-mini--installer-source-git.md)), there's enough information to give every installed extension a real status. This ticket is the output reformat that uses it.

## Proposed output shape

Categories match the source-type taxonomy from the [parent design](2026-05-13--cc-mini--installer-registry-source-types-architecture.md). Note: `local` is descoped this iteration (the type exists in the schema, but local-path tracking is not implemented); any local-installed extension uses `type: "private"` for now.

The `Untracked extensions` section was introduced in [Phase 1](2026-05-13--cc-mini--installer-source-npm-honest-cleanup.md). This Phase 2 reformat preserves it; the migration command moves entries OUT of `Untracked` and INTO the right category over time.

```
LDM OS v0.4.85-alpha.NN
Installed: 2026-05-13
Updated:   2026-05-13
Extensions: 32

Update summary:
  npm:       20 tracked, 6 updates available
  git:        5 tracked, 1 update available
  bundled:    4 tracked (update via parent)
  private:    3 tracked (auto-check disabled)
  untracked:  0 (run `ldm doctor --reclassify-sources` if any)

Updates available (7):
  wip-repos          1.9.69  ->  1.9.70   (@wipcomputer/wip-repos, npm)
  wip-file-guard     1.9.69  ->  1.9.70   (@wipcomputer/wip-file-guard, npm)
  ...
  root-key           0.2.0   ->  0.3.0    (wipcomputer/wip-root-key, git)

Bundled extensions:
  lesa-bridge        0.3.0   (updates with @wipcomputer/wip-ldm-os)
  wip-release        1.9.79  (updates with @wipcomputer/wip-ai-devops-toolbox)
  ...

Ahead of upstream (1):
  openclaw-tavily    1.0.1   (ahead of wipcomputer/openclaw-tavily v0.2.1, git)

Private extensions (auto-check disabled):
  compaction-indicator   1.0.1
  ...

Untracked extensions (pending reclassification):
  (none ... run `ldm doctor --reclassify-sources` if entries appear here)

Probe failures (0):
  (none)

Run: ldm install
```

Key changes from today's output:

- Every installed extension appears exactly once, in one of: updates-available, bundled, ahead-of-upstream, private, untracked, or probe-failures.
- The legacy skipped section becomes `probe-failures` — and is only for actual probe failures (gh API down, network unreachable). Intentional opt-outs land in `private`. Pending-classification entries land in `untracked`.
- Source type label after each row uses the schema field name (`npm`, `git`, `bundled`, etc.) consistently. No `github`/`gh` synonyms.
- Counts at the top reflect every registered extension.
- "Ahead of upstream" is a separate section for forks where local exceeds upstream; not framed as an update available.

### `source.local` and `source.private` minimal implementations

- `type: "local"`: **rejected by the schema validator this iteration.** Per the round-3 reviewer consensus, since local has no probe code and no path tracking, accepting it would create a contradiction with the "exactly one row per registry entry" promise above (local entries had no section to land in). Rejecting at the validator removes the contradiction. No real-world entry uses `local` today. When local-path tracking lands in a future iteration, the validator's allow-list expands to re-admit `local` and this ticket's acceptance gets updated to define the row treatment then.
- `type: "private"`: registry entry is accepted. `ldm status` skips probing. Rows appear in the `Private extensions (auto-check disabled)` section.

## Edge cases to design for

- **Probe failure on an npm-source extension:** moves to `probe-failures` section with reason, doesn't disappear from the table.
- **Bundled extension whose parent had a probe failure:** report as bundled, but include a `(parent probe failed)` note.
- **Phantom registry entry whose directory is missing:** ([registry hygiene ticket](2026-05-13--cc-mini--installer-registry-hygiene-audit.md)). Report as `probe-failures` with `[phantom: directory not found]` reason.
- **Extension with no source at all** (mystery entries like the current `run` row): report as `probe-failures` with `[no source]` reason.
- **Fork:** local version newer than upstream's latest tag. Appears in `Ahead of upstream` section, not in `Updates available`.

## Acceptance

- Every registry entry produces exactly one row in `ldm status` output.
- Rows are grouped by `updateSource.type` (npm/git/bundled/private) plus the `Ahead of upstream`, `Untracked`, and `Probe failures` non-source sections.
- No silent drops. No empty omissions.
- The `probe-failures` section is only for unexpected failures, not for intentional opt-outs (which land in `private`) and not for pending-classification entries (which land in `untracked`).
- Source labels in user-facing strings match the schema field names exactly: `npm`, `git`, `bundled`, `private`, `untracked`. Not `github`/`gh` synonyms. (`local` is rejected by the validator this iteration; see below.)
- **`local`-type entries are rejected by the validator this iteration.** No row produced, no summary line, no count. The `local` type remains in the schema for forward compatibility but is on the validator's deny-list until local-path tracking ships.
- `private`-type entries land in the `Private extensions (auto-check disabled)` section. Never in `probe-failures`.
- `untracked`-type entries (carried over from Phase 1) land in the `Untracked extensions` section with a `ldm doctor --reclassify-sources` remediation hint.
- **Phase 1 defensive silent-skip MUST be removed.** Phase 1 of the source-types refactor introduced a defensive `continue` in `cmdStatus` (`bin/ldm.js`) for any `updateSource.type` that is neither `npm` nor `untracked`, to prevent legacy fallthrough to `info.source.npm` when a hand-edit introduced a non-npm type before Phase 2 shipped. That skip exists ONLY because no other types could legitimately appear during the Phase 1 window. When this ticket's per-type dispatch lands, the skip becomes a violation of "every installed extension appears exactly once" ... it would silently hide `git`/`bundled`/`private` entries. The dispatch implementation MUST delete the Phase 1 skip block (look for the comment `Defensive skip for any other Phase 2 updateSource types`) and replace it with the proper per-type rendering this ticket defines. Captured here as a hand-off note from the cc-reviewer + codex-reviewer review of PR #938.
- Regression test: stage a fixture registry with one entry of each accepted source type (npm/git/bundled/private/untracked) plus one fork (local > upstream) and one probe-failure (gh API mocked to 503). Assert all rows appear in correct categories.
- Regression test: stage a fixture entry with `updateSource.type: "local"`; assert the validator rejects it with a clear error message.
- Regression test: stage a fixture entry with `updateSource.type: "git"` and `updateSource.type: "bundled"`; assert each lands in the correct section (not silently skipped). This is the regression guard for the Phase 1 defensive-skip removal above.

## Why P2

Output formatting is downstream of the schema (Steps 1-3). After the schema work lands, this ticket consolidates the output. Could ship in the same alpha as Step 3 (source.git) since they're co-dependent.

## Out of scope

- A separate `ldm status --json` shape. Already exists today and returns the top-level summary only. Could be expanded in a follow-up to expose the full source-type-categorized data structure.

## Recommendation

Alpha after fix. Dogfood install prompt; verify the report finally shows everything you have, clearly.

## Related

- Parent: [Installer registry source types architecture](2026-05-13--cc-mini--installer-registry-source-types-architecture.md)
- Depends on: Step 1 cleanup, Step 2 bundled, Step 3 git
- Master ticket: [ldmos-bugs-masterticket--installer.md](ldmos-bugs-masterticket--installer.md)
