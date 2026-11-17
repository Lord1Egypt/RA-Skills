---
title: Finish dev guide path migration (consumers + lint + remove compat write)
date: 2026-04-30
status: ticketed
severity: P3
component: ldm-installer | dev-guide | claude-rules | agent-boot
discovered-via: PR #766 verification (corrected diagnosis from branch-prefix inconsistency ticket)
related-prs: PR #768 (immediate compat-write fix)
co-authors: Parker, Lesa, Claude
---

# Finish dev guide path migration

## Observed

The 2026-04-19 deploy migration moved `dev-guide-wipcomputerinc.md` from `~/.ldm/shared/` to `~/.ldm/library/documentation/` as the canonical deploy target, but stopped short of:
1. Moving consumer references to the new path.
2. Removing or stubbing the leftover old file.
3. Auditing other `~/.ldm/shared/` files for the same pattern.

PR #768 (this same date) added a migration-window compatibility write so both paths now serve current content. That's the immediate stale-copy safety fix. **This ticket scopes the forward migration that PR #768 deliberately did not include.**

## Expected

After forward migration:
- Every reference to `~/.ldm/shared/dev-guide-wipcomputerinc.md` in consumer files updated to `~/.ldm/library/documentation/dev-guide-wipcomputerinc.md`.
- The old shared path is either removed, redirect-stubbed, or doctor-flagged. Old-path readers either follow the redirect or surface a warning.
- `deployDocs()` no longer writes the compat copy at the old path (the line added in PR #768 is removed).
- Any other `~/.ldm/shared/<file>` that has the same half-migration pattern is identified and either migrated forward or explicitly left in place with a documented reason.
- `ldm doctor` flags future split-path drift automatically.

## Impact

- **Stale policy distribution risk recurs** if PR #768's compat write is reverted before consumers are migrated. Forward migration removes that risk durably.
- **Discoverability:** consumers that read the dev guide via grep/find scans will see two paths and need to know which is canonical.
- **Future migrations of the same shape** will hit the same trap unless the lint check (item 5 below) lands.
- **No live runtime impact** as long as PR #768's compat write is in place. Both paths serve current content. This ticket is preventive/cleanup work.

## Evidence

- PR #766 corrected diagnosis: source template correct, old deploy path stale.
- PR #768: compat write at deployDocs() level. Now both `~/.ldm/library/documentation/dev-guide-wipcomputerinc.md` and `~/.ldm/shared/dev-guide-wipcomputerinc.md` get refreshed by `ldm install`.
- `bin/ldm.js:730-733` original comment from 2026-04-19: "this change moves one file cleanly into the new location without pre-empting the broader migration."
- Likely consumers of the old path (incomplete; full grep is part of the work):
  - `~/wipcomputerinc/CLAUDE.md`
  - `~/.claude/CLAUDE.md`
  - `~/.claude/rules/release-pipeline.md` and other rules files
  - `~/.openclaw/workspace/AGENTS.md`, `CONTEXT.md`, `TOOLS.md`, `SHARED-CONTEXT.md`
  - Other repo CLAUDE.md files that mention the dev guide
  - Templates under `wip-ldm-os-private/shared/docs/*.tmpl` that may cross-reference

## Root cause

A migration that was scoped narrowly (move one deploy target) was never followed by the consumer-side cleanup. The original comment in `bin/ldm.js` even named this gap explicitly ("the broader migration is pending"), but no ticket tracked the broader work and no `ldm doctor` check would surface it later.

## Fix plan

**Scope to decide before any sweep:**

1. **Survey all consumers of `~/.ldm/shared/dev-guide-wipcomputerinc.md`.** Run a grep across every relevant tracked private repo and the operator's home dirs. Targets to include in the grep:
   - `~/wipcomputerinc/CLAUDE.md`, `~/.claude/CLAUDE.md`, `~/.claude/rules/*.md`
   - `~/.openclaw/workspace/AGENTS.md`, `CONTEXT.md`, `TOOLS.md`, `SHARED-CONTEXT.md`
   - Every CLAUDE.md and README in `~/wipcomputerinc/repos/ldm-os/`
   - All `*.tmpl` files in `wip-ldm-os-private/shared/docs/` (cross-references inside templates)
   - Installed extensions under `~/.ldm/extensions/*` and `~/.openclaw/extensions/*`

2. **Update each reference** found in step 1 from `~/.ldm/shared/dev-guide-wipcomputerinc.md` to `~/.ldm/library/documentation/dev-guide-wipcomputerinc.md`. Land per-repo PRs to keep diffs scoped.

3. **Decide what to do with the old shared file.** Three options, in order of safety:
   - **(a) Compatibility stub.** Replace the file content with a one-line pointer. Old-path consumers see the redirect and update at their pace.
   - **(b) Doctor-flagged but not removed.** Leave file in place; `ldm doctor` warns when stale references exist anywhere on disk.
   - **(c) Remove.** Highest risk; could break agents whose boot contract still references it. **Parker's recommendation: do not delete blindly.**
   - Recommend (a) at deploy time after consumers are migrated, not before.

4. **Audit other `~/.ldm/shared/` files for the same half-migration pattern.** Compare every `*.tmpl` under `wip-ldm-os-private/shared/docs/` against any matching deployed file at both `~/.ldm/shared/` and `~/.ldm/library/documentation/`. Sample candidates that may have analogous drift:
   - `acknowledgements.md.tmpl`
   - `directory-map.md.tmpl`
   - `how-agents-work.md.tmpl`
   - `how-backup-works.md.tmpl`
   - `how-install-works.md.tmpl`
   - `how-releases-work.md.tmpl`
   - `how-rules-and-commands-work-placeholder.md.tmpl`
   - `how-web-skills-work-placeholder.md.tmpl`
   - `how-worktrees-work.md.tmpl`
   On this machine 2026-04-30, only `dev-guide-wipcomputerinc.md` had a leftover at `~/.ldm/shared/`. The other templates may be fine. Audit confirms.

5. **Add an `ldm doctor` lint check** that compares source templates against deployed files at both old and new paths. Flag drift in either direction. Generalizes the catch from PR #766 and prevents the next migration from reproducing this pattern silently.

6. **Remove the migration-window compat write from `deployDocs()`** (the lines added in PR #768) once steps 1-5 are confirmed done. The compat write is explicitly temporary; this ticket tracks its end-of-life.

## Test plan

After the consumer-migration PRs + compat-stub:

- [ ] Every consumer reference updated. Re-grep the targets in step 1; expect zero matches against the old path (or only matches that are explicit historical citations).
- [ ] `~/.ldm/shared/dev-guide-wipcomputerinc.md` is either a one-line redirect, doctor-flagged, or absent (per option chosen in step 3).
- [ ] `ldm install` is a no-op for the compat write (line removed from `deployDocs()`).
- [ ] An agent that boots and reads via the old path either follows the redirect or surfaces a doctor warning.
- [ ] `ldm doctor` lint check passes on the current state and fails when an artificial stale file is introduced.

## Smoke test

```bash
# Verify canonical path still correct
grep -n "Branch Prefix" ~/.ldm/library/documentation/dev-guide-wipcomputerinc.md
# expect: oc-lesa-mini/

# Verify old path's chosen disposition
head -3 ~/.ldm/shared/dev-guide-wipcomputerinc.md
# expect: redirect message OR no such file (depending on chosen option)

# Verify no stale references remain
grep -rln "\.ldm/shared/dev-guide-wipcomputerinc" ~/wipcomputerinc/CLAUDE.md ~/.claude/ ~/.openclaw/workspace/ 2>/dev/null
# expect: empty

# Verify lint catches future drift
ldm doctor
# expect: doc-drift check passes; if a stale shared file is introduced, doctor flags it
```

## CC review request

- Is option (a) compatibility stub the right disposition for the old shared file? Parker leaned that way; lesa-work-02 also flagged "do not delete blindly."
- Should the consumer survey + migration land as one big PR or split per repo?
- Should the `ldm doctor` lint be its own ticket, bundled into the migration PR, or part of a separate doctor-hygiene effort?
- Are there other `~/.ldm/shared/` files that should also stop being a deploy target alongside the dev guide cleanup?

## Release path

Multi-repo docs change. Each consumer repo PRs independently. After all consumer PRs merge, a final `wip-ldm-os-private` PR removes the compat write from `deployDocs()`. The compat write should be the LAST thing to go, so consumers don't briefly fail during the transition.

Alpha track for the final code change (removal of compat write). Operator must be on the new path before the compat write is removed.

## Rollback

If the migration breaks a consumer:
- Re-add the compat write to `deployDocs()` (revert the cleanup PR).
- Restore the old path's content from the canonical file: `cp ~/.ldm/library/documentation/dev-guide-wipcomputerinc.md ~/.ldm/shared/dev-guide-wipcomputerinc.md`.
- Open a fresh ticket for the broken consumer.

## Why P3

No live system is currently failing. PR #768 keeps both paths serving current content. Forward migration is preventive cleanup, not bleeding-fix. Worth doing in a quiet moment before the next migration of the same shape compounds the drift.

## References

- PR #766 (merged): branch-prefix inconsistency ticket. Its corrected diagnosis surfaced this.
- PR #768 (open as of 2026-04-30): compat write that closes the immediate stale-copy issue.
- `bin/ldm.js:730-733` original migration comment.
- KNOWN-LANDMINES candidate (per lesa-work-02's review of #766): "stale `~/.ldm/shared/<doc>` may persist after migrating that doc to `~/.ldm/library/documentation/`. Always check both paths."

## Out of scope

- The compat write itself (PR #768 ships it).
- The branch-prefix correctness in the dev guide (PR #766 + the source template already handle that).
- The upstream OpenClaw TUI delivery-mirror PR (#75195 in `openclaw/openclaw`); separate surface, lesa-work-02 owns.
- Lēsa's lane workflow (`bugs/lesa/`, `plans-prds/current/lesa/`); separate concern.
