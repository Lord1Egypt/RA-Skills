# Maintenance Reference — Super Memori v4

> ⚠️ **This file is extracted from the SKILL.md `<details>` maintenance block.**
> Human maintainers only. Weak models must not use this during normal operation.

<details>
<summary>⚠️ MAINTENANCE — DO NOT EXPAND DURING NORMAL USE — HUMAN USE ONLY ⚠️</summary>

> ⚠️ SCOPING DISCLAIMER: All text inside this block is frozen maintenance context at packaging time (`v4.0.0-candidate.23`). It does not override the active operating contract, health gates, or exit-code rules above. Weak models must treat it as historical/reference material, not live runtime truth.

## Execution Notes

> ⚠️ This block is HUMAN / MAINTENANCE ONLY. Weak models must not expand it during normal operation.
> ⚠️ All content below is frozen maintenance reference captured at `v4.0.0-candidate.23`. Do not treat it as active operating contract.
> Active mode selection, health gates, and execution rules are fully defined in the Runtime Capability Matrix and Implemented vs Optional sections above.
> This section contains reference material, future-spec mapping, and migration notes only.

## Core Position

Build memory like an operating system component, not like a demo.

Maintenance assumptions for this skill:
- **Files are canonical truth**
- **SQLite FTS5 handles exact / lexical retrieval**
- **Qdrant handles semantic retrieval when available**
- **A small CPU reranker is optional quality lift, not the foundation**
- **Weak models should stay on the 4-command public interface**

Everything else in this block is maintenance-only reference material for improving the skill rather than using it.

## Retrieval Contract [REFERENCE ONLY — DESCRIBES CURRENT V4 RUNTIME SHAPE, NOT A MANUAL EXECUTION PLAN]

> ⚠️ This describes the current v4 retrieval pipeline shape as implemented inside `query-memory.sh`. Do not reconstruct, simulate, or manually sequence these steps.

The current v4 retrieval path is:

```text
query
  → filters (type, time, tags, namespace)
  → lexical retrieval (SQLite FTS5)
  → semantic retrieval (Qdrant, when available / needed)
  → fusion
  → optional rerank
  → deduplicate / diversify
  → results + warnings + freshness state
```

**Health integration:** `query-memory.sh` already surfaces degraded state in its output. You do not need to run `health-check.sh` before every query. Use `health-check.sh` before major memory surgery, after suspicious behavior, or when you need to confirm whether degraded results are still trustworthy.

## Write / Learning / Change-Memory Contract (target behavior)

Use `memorize.sh` only when the new information is likely to help future runs.

### What learning memory is for
Learning memory is the scratch lane for self-improvement:
- reusable failures
- corrections
- lessons
- recurring anti-patterns
- meaningful capability gaps
- recurring retrieval misses
- repeated success patterns worth operationalizing
- stale or superseded lessons that should be reviewed

Learning memory is not durable truth by default. It must earn promotion after repeated reuse or explicit permanence signals.
Repeated signals should be aggregated into reviewable pattern reports instead of staying as isolated notes.

### Change-memory operational rules
- Treat change-memory as operational truth for agent-made changes, not as a substitute for direct live inspection when exact current machine state is required.
- A minimal hot-change-buffer may retain very recent recovery-only event records for interrupted runs and recent-change recall; it is not canonical truth, not durable truth, and not exact current machine state.
- Do not present `reverted` or `unverified` change records or hot events as active current state.
- Harmless reads must not be logged as change-memory events or hot-buffer events.
- Log only state-changing actions, failed writes, risky cleanup, package/service/config/runtime changes, rollback events, and recent multi-step risky change boundaries.

### Before major memory work
Major work = policy edits, index changes, mass rewrites, command-contract changes, retrying a previously failed memory task, or editing `SKILL.md`, references, or public scripts for this skill.
1. Run `./health-check.sh`. If status is `FAIL`, stop. If status is `WARN`, continue only with explicit degraded-mode awareness and a rollback path.
2. Verify rollback exists (`git status`, backup directory, or untouched canonical files).
3. Run `./query-memory.sh --mode learning --limit 5` and reuse any clearly matching lesson.
4. If learning quality or repeated misses matter, run `python3 mine-patterns.py` before changing promotion policy, retrieval logic, or memory structure.
5. If the pattern report shows stale-success candidates, recurring misses, or related lesson clusters, review them manually before patching or proposing promotion.
Read `references/learning-improvement.md` when you need the full pattern-mining workflow. Purpose: run promotion/retrieval review safely.

### Good candidates
- an unexpected failure with a reusable lesson
- a user correction that changes future behavior
- a better repeatable procedure
- a recurring anti-pattern
- a meaningful knowledge gap

### Bad candidates
- expected no-match results
- one-off noise
- weak guesses
- duplicate lessons already recorded
- `checked, nothing relevant`

### Promotion to durable memory

**DO NOT PERFORM PROMOTION.** Promotion is maintenance-only/manual review in the current v4 candidate line, not an automated runtime command.

For the current skill:
- **Promotion is manual. Do not auto-promote.**
- `memorize.sh` writes stay in learning memory.
- If a learning seems durable, say only: `Learning <summary> appears valuable for later manual promotion.`
- If repeated lessons, corrections, misses, or successful reuse signals appear related, aggregate them through `python3 mine-patterns.py` before proposing manual promotion.
- Use the same pattern report to identify retrieval-quality issues before changing indexing or degraded-mode rules.
- If reuse evidence is stale, verify it manually before treating it as current best practice.

### Durable target mapping (manual review mapping, not active runtime automation)
Promotion into procedural or semantic memory is a manual maintenance layer, not a fifth public command.
No current runtime command performs this promotion automatically.
If a human-approved manual promotion exists later, use this mapping:
- repeatable commands / debugging steps → procedural memory
- anti-patterns / post-mortems → procedural lessons memory
- durable facts / preferences / infrastructure facts → semantic memory
- decisions with rationale → semantic decisions memory

### Anti-patterns
- Do not auto-log every non-zero exit code.
- Do not duplicate the same lesson in multiple learning records.
- Do not promote one-off context into durable memory.
- Do not attempt to promote learnings without human action.
- Do not invent commands for promotion.
- Do not log that nothing relevant was found.

## Health / Freshness Contract

Health is not only about indexes. Health also means the agent can tell whether learning-memory is being used honestly instead of as a dumping ground, whether degraded mode is safe to continue in, and whether the host-side conditions still support trustworthy memory work.

`health-check.sh` currently reports at least:
- canonical files readable
- lexical index status
- semantic index status
- queue backlog
- last successful index update / freshness state
- degraded state

Advanced checks such as duplicate / orphan risk belong to the fuller semantic layer and should not be claimed until runtime support exists.

`query-memory.sh` currently reports at least:
- `mode_requested`
- `mode_used`
- `degraded`
- `warnings[]`
- `index_fresh`
- `results[]`

`--reviewed-only` excludes learning entries marked `- status: pending`. Grep fallback respects this behavior too.

### Memory-safe operation rules
- Follow the `WARN` vs `FAIL` rules from the Memory Health Contract before relying on results.
- Before major memory surgery, confirm a rollback path exists and is accessible (`git status`, backup directory listing, or verified canonical file copies).
- Prefer reversible changes to indexing, health scripts, and retrieval contracts.
- Do not schedule recurring maintenance or audits without explicit approval.

## Current Folder Meaning [MAINTENANCE REFERENCE — ARCHIVED AT v4.0.0-candidate.23; CURRENT STABLE: 4.0.1]

### Active public entrypoints
- `query-memory.sh`
- `memorize.sh`
- `index-memory.sh`
- `health-check.sh`

These implemented the v4.0.0-candidate.23 local-only runtime at packaging time: lexical retrieval is active by default, semantic/hybrid retrieval exists in code, and host state determines whether semantic/hybrid can activate on this machine.
This block is historical packaging context, not the current release-state authority. The active stable line is now `4.0.1`; use `SKILL.md`, `references/release-status.md`, and live command outputs for current truth.
Promotion-to-durable-memory remains maintenance-only/manual review. The stable-host readiness gate described below is archived historical context for the pre-`4.0.1` promotion path, not pending work for the current stable line.

### Maintenance-only entrypoints and support surfaces
- `audit-memory.sh`
- `repair-memory.sh`
- `list-promotion-candidates.sh`
- `validate-release.sh`
- `validate-equipped-host.sh`
- `mine-patterns.py`
- `auto-learner.sh`
- `references/`

These are maintenance-only. Weak models must not open or inspect them during normal query/memorize/index/health operations.
Only read or run them when an explicit maintenance step says `Read ...` or `Run ...`.

### Legacy baseline (`scripts/legacy/` + archive material)
These preserve older v2/v3-era behavior as historical reference only.
They are not the current runtime truth.

### Current references
Detailed v4 architecture, contracts, release-state, and host-readiness surfaces live in the `references/` directory. Human maintainers should consult those files when improving the current stable line, while treating explicitly archived candidate-era sections as historical only.

## Backup / Exposure / Risk Notes

- Files remain the canonical recovery path if indexes degrade or semantic dependencies disappear.
- If the host is remote, exposed, or lightly backed up, prefer plan-first changes over direct edits to memory scripts.
- If backups or snapshots are unknown, assume caution and avoid irreversible cleanup.
- Health guidance for this skill covers memory reliability, not full host hardening. Use `healthcheck` for broader host security decisions.

## How to use this skill today

### If you need current memory behavior
Use the active root commands:
- `query-memory.sh`
- `memorize.sh`
- `index-memory.sh`
- `health-check.sh`

### If you are improving the skill
Do this order:
1. Run `health-check.sh`
2. Review recent learning-memory if the task is major or previously failed
3. Confirm whether rollback exists (git, backup, untouched canonical files)
4. Read `references/architecture.md`
5. Read `references/command-contracts.md`
6. Read `references/migration-plan.md`
7. For learning-quality or promotion-policy work, run `python3 mine-patterns.py` and read `references/learning-improvement.md`
8. Review both promotion candidates and retrieval-audit signals from the pattern report
9. Check whether repeated successful reuse signals change the promotion decision
10. Check whether stale success candidates or cooling clusters require manual re-validation
11. Only then patch or replace scripts
12. Re-run health after the patch

## Design target [MAINTENANCE REFERENCE — HISTORICAL CONTEXT]

The goal is not “the fanciest memory system”.
The goal is:

> **the strongest honest local-only memory skill that weak models can use reliably on a CPU-only Ubuntu OpenClaw host**

That was the packaging bar for the `v4.0.0-candidate.23` candidate line. Current runtime behavior and live health gates override this reference if host state diverges.

## Release interpretation [MAINTENANCE REFERENCE — ARCHIVED]
> ⚠️ ARCHIVED: This promotion path was completed for `4.0.1`. Treat the candidate-era notes below as historical reference, not pending work.

- **Historical v3 line (`3.x`)** = lexical-first baseline with degraded semantic reporting and a smaller runtime claim surface
- **Archived candidate snapshot (`4.0.0-candidate.23`)** = historical v4 candidate state where lexical, semantic, hybrid, temporal-relational, audit, change-memory, and change-audit capabilities existed in code while learning-improvement surfaces remained maintenance-only and host-state activation could still be degraded on a given machine
- **Current stable line (`4.0.1`)** = the first equipped-host-verified stable release state for the current-generation local-only runtime, with current host execution truth still read from live command outputs rather than inferred from the release label alone

## Stable-release gate [HUMAN/MAINTENANCE ONLY — ARCHIVED]

> ⚠️ ARCHIVED: This promotion path was completed for `4.0.1`. Keep this checklist only as historical evidence of the pre-stable gate; do not treat it as pending work for the current stable line.
>
> ⚠️ This is a stable-release verification checklist for already-implemented runtime features on an equipped host. Weak models must not execute, track, or report on these steps.

Do not skip steps **when verifying on an equipped host**.
1. [ ] `health-check.sh --json` shows lexical baseline healthy
2. [ ] semantic prerequisites are installed and verified on an equipped host
3. [ ] semantic / vector indexing for canonical files is verified on an equipped host
4. [ ] semantic freshness / backlog state is visible and healthy on an equipped host
5. [ ] `query-memory.sh --mode hybrid` is verified on an equipped host to fuse lexical + semantic results
6. [ ] optional reranker, if enabled, is healthy on an equipped host and documented honestly
7. [ ] docs, runtime, and health semantics all align before any 4.0.0 stable release

For the short archived promotion instruction, read `references/roadmap-to-4.0.0.md` as historical context only.

</details>
## Maintenance Anti-Patterns (human reference)

When editing this skill, do not:
- claim semantic retrieval is fully active on the current host unless dependencies, local model, vectors, and health checks actually pass
- add more public commands for weak models
- make Qdrant the canonical source
- let degraded lexical-only mode fail silently
- log harmless reads as change-memory events
- auto-log every non-zero exit code as a lesson
- treat repeated failures as isolated one-off notes when they should be aggregated into pattern reports
- ignore retrieval-audit signals when pattern mining shows recurring misses, lexical fallbacks, or fragmentation hints
- ignore repeated successful reuse when deciding whether a procedure or lesson deserves manual promotion review
- treat stale success as current truth without manual re-validation
- auto-promote pattern clusters without human review
- schedule recurring checks or maintenance without explicit approval
- mix architecture notes back into the public command interface

