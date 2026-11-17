# Plan: Ship all 8 phases of the Crystal Resilience Plan

**Save target:** after approval, copy this plan to
`/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/bugs/memory-crystal/2026-04-13--cc-mini--ship-plan-resilience-phases.md`
so the plan lives alongside the bug reports it implements.

## Context

The Crystal Resilience Plan (merged in PR #585) lists 8 phases of work to close ingestion gaps exposed by the Apr 11-12 outage. Parker asked me to "fix as you see fit," and I've been working through Phases 5 and 6a.

**Phase 5** (model_id column on memory-crystal chunks) is already merged to main: PR #114, commit `f216046`. The source change is done. It's not yet on npm, so no user is running it. The next step is `wip-release` to publish the alpha, then `ldm install` (by Parker, on signal) to deploy.

**Phase 6a** (OpenClaw format-error billing cooldown fix) was scoped as a classifier change in `src/agents/pi-embedded-helpers/errors.ts`. Before patching, I asked an Explore agent to find the Apr 11-12 log evidence. The evidence changed the picture, so Phase 6a should hold until we re-investigate.

Parker's two-layer architecture (confirmed with him):
- **Layer 1 — OpenClaw fork**: upstream → rebase our patches onto new tag → `npm link` from the worktree. Patch Tracking table in `open-claw-upgrade-private/UPGRADE-RUNBOOK.md` is the manifest.
- **Layer 2 — LDM OS**: components publish to npm → `ldm install` pulls and deploys to `~/.openclaw/extensions/` and `~/.ldm/`.

These two layers deploy separately.

**Install policy (clarified by Parker):**
- **Alpha tracks: install freely.** Alpha is for dogfooding and iteration. Deploy → install → verify is the normal loop.
- **Beta / stable releases: Parker's explicit signal required.** Those are the careful dogfood gates.

## Hard constraints (rules I will not break)

- **`openclaw doctor` must always work.** Any patch to the OpenClaw fork must not break OpenClaw's own internal functionality. Patches add on top; they do not replace or remove core behavior. If `doctor` can't run after a patch, the patch is wrong.
- **The install flow is: clone our fork (patches already rebased onto upstream) → install from that fork → `doctor` verifies.** Our patches are baked in because they're already in the fork's branch. The installer does not apply patches separately at install time; it installs the already-patched build.
- **Never touch deployed files directly.** `~/.ldm/`, `~/.openclaw/`, `~/.claude/` are outputs of the installer, not inputs. The repo is the source of truth.
- **Merge, Deploy, Install are three separate steps. Never combine.** Parker signals when to move between them.

## New evidence on Phase 6a (from gateway logs)

The Apr 11 auth profile for Anthropic went from `reason=format` at 13:35 to `reason=billing` at 21:50 UTC. **No log entry shows a conversion from format→billing.** The message text of the format error was:

> `messages.101: tool_use ids were found without tool_result blocks immediately after...`

That text contains no billing keywords, so the message-content classifier (`errors.ts:671-748`) would not have flipped it to billing. The HTTP-status classifier (`errors.ts:610-618`) correctly returned `format`.

The most likely explanation: a **separate, real billing event** (running out of "extra usage" metered credits) happened between 17:41 (last format entry in logs) and 21:50 (first billing entry). That would have correctly set `disabledReason: "billing"`.

Implication: the bug report title "format errors incorrectly cooldown auth profiles" may be misattributing the cooldown. Without a confirmed repro of the misclassification path, patching the classifier is speculative and could break legitimate billing failover.

## Plan

### Step 1. Deploy Phase 5 (memory-crystal alpha)

Run from main of `memory-crystal-private`:

```bash
cd /Users/lesa/wipcomputerinc/repos/ldm-os/components/memory-crystal-private
git pull --ff-only  # sync to 9602527 (PR #114 merged)
wip-release alpha --dry-run  # preview
# If preview is correct:
wip-release alpha --notes="feat(chunks): model_id column for cross-model provenance. Backfills existing dbs via idempotent ALTER TABLE. Populated from msg.model in OpenClaw agent_end hook and CC session poller."
```

**What this does:**
- Bumps `package.json` version `0.7.34-alpha.4` → `0.7.34-alpha.5`
- Generates CHANGELOG entry
- Commits + tags `v0.7.34-alpha.5`
- Publishes to npm @alpha tag (`@wipcomputer/memory-crystal@0.7.34-alpha.5`)
- Creates GitHub release
- No public notes (alpha track default)
- No `deploy-public.sh` (alpha prerelease default)

**Blast radius:**
- npm: new version appears (existing versions untouched)
- GitHub: new tag + release
- Parker's machine: NOTHING changes. No extensions updated. Gateway untouched.
- Reversible: `npm unpublish @wipcomputer/memory-crystal@0.7.34-alpha.5` within 72 hours; `git push origin :v0.7.34-alpha.5` to drop tag.

### Step 1b. Install the alpha via `ldm install`

Since this is an alpha (dogfood track), install without waiting:

```bash
ldm install memory-crystal      # or the equivalent flag that targets a single extension
# If no per-extension flag, `ldm install` may pull all alpha-tracked components.
openclaw gateway restart        # re-init so the ALTER TABLE migration runs
```

**What this does:**
- Pulls `@wipcomputer/memory-crystal@0.7.34-alpha.5` from npm
- Deploys to `~/.openclaw/extensions/memory-crystal/`
- Gateway restart re-runs `crystal.init()`. The idempotent `ALTER TABLE chunks ADD COLUMN model_id TEXT` runs once; subsequent boots swallow the duplicate-column error.
- New agent turns start populating `model_id` from `msg.model`.
- Existing ~91.6K chunks get `model_id = NULL` (acceptable — they pre-date the column).

**Verify:**
```bash
openclaw doctor                 # must complete clean
sqlite3 ~/.openclaw/memory/crystal.db "PRAGMA table_info(chunks);" | grep model_id
# Should show: model_id|TEXT

# After a few turns, verify new chunks populate it:
sqlite3 ~/.openclaw/memory/crystal.db "SELECT id, model_id FROM chunks ORDER BY id DESC LIMIT 5;"
# Recent rows should show model_id = 'claude-sonnet-4-6' (or whatever Lēsa's on)
```

**Rollback if broken:**
```bash
# Revert to previous alpha
ldm install memory-crystal@0.7.34-alpha.4
openclaw gateway restart
# The ALTER TABLE is forward-compatible; no DB rollback needed. The new column becomes vestigial on the older build.
```

### Step 2. Hold Phase 6a. Update the bug report instead.

Do NOT patch OpenClaw's classifier. The log evidence doesn't support the hypothesis that a format error was misclassified as billing. Instead:

Open a small PR to `wip-ldm-os-private` appending an "Investigation Update" section to:
- `ai/product/bugs/openclaw/2026-04-12--cc-mini--format-error-billing-cooldown.md`

The update records:
- Gateway log timeline (13:35 format → 17:41 last format entry → 21:50 first billing entry, no conversion log)
- Format error message text (no billing keywords)
- Revised hypothesis: separate "extra usage exhausted" billing event, not a misclassification
- Next-investigation steps: dump auth-state.json history around 21:50; grep session files for billing-esque error messages between 17:41 and 21:50; check if Parker's Anthropic extra-usage credits hit zero that evening

This is a documentation change on a PR branch, merged normally. Nothing deployed. Nothing installed.

### What this plan does NOT do

- No `npm link` from OpenClaw fork worktree.
- No edits to OpenClaw source (no `errors.ts` patch).
- No new row in `open-claw-upgrade-private/UPGRADE-RUNBOOK.md` Patch Tracking table (nothing to track).
- No edits to `post-upgrade-patches.sh`.
- No direct edits to `~/.ldm/`, `~/.openclaw/`, `~/.claude/` (the ldm installer is the only writer).
- No `openclaw doctor --fix` (read-only `openclaw doctor` for verification is fine).
- No beta or stable release. Alpha only.

## Files the plan touches

### Step 1 (via wip-release automation):
- `repos/ldm-os/components/memory-crystal-private/package.json` (version bump)
- `repos/ldm-os/components/memory-crystal-private/CHANGELOG.md` (append entry)
- git tag `v0.7.34-alpha.5`
- npm registry: new version published

### Step 2 (manual edit on PR branch):
- `repos/ldm-os/wip-ldm-os-private/ai/product/bugs/openclaw/2026-04-12--cc-mini--format-error-billing-cooldown.md` (append section)

## Verification

**After any OpenClaw-touching work (future Phase 6a or similar):**
```bash
openclaw doctor
# Must complete without errors. If doctor breaks, revert the patch.
```

**After Step 1:**
```bash
npm view @wipcomputer/memory-crystal versions --json | tail -5
# Should include "0.7.34-alpha.5"

git -C /Users/lesa/wipcomputerinc/repos/ldm-os/components/memory-crystal-private log --oneline -3
# Should show the wip-release bump commit + tag

# On Parker's running system — NOTHING should have changed:
openclaw extensions list | grep memory-crystal
# Should still report the currently-installed version (not alpha.5)
```

**After Step 2:**
```bash
gh pr view <N> --json state,mergedAt
# Shows PR merged
```

## Remaining phases (3 through 8 of the Crystal Resilience Plan)

These are the other phases from `ai/product/plans-prds/current/memory-crystal/2026-04-12--cc-mini--crystal-resilience-plan.md`. Each has a Layer (1 = OpenClaw fork, 2 = LDM OS extension), a priority order from the plan, and a blast-radius note.

Layer-2 phases (no OpenClaw source change — lower risk, ship independently):

### Step 3. Phase 2 — iMessage chat.db fallback ingestion (Layer 2)

- **What:** Secondary ingest source that reads `~/Library/Messages/chat.db` on a 5-minute sweep. Crystal captures messages even when OpenClaw can't produce an `agent_end` event.
- **Files:** new `src/chatdb-poller.ts` in `memory-crystal-private` + registration in `src/openclaw.ts` + new capture-state row.
- **Risk:** contained to memory-crystal extension. Privacy filter on `allowFrom` handles. chat.db schema is stable across macOS versions we ship on.
- **Ship:** new branch → PR → merge → `wip-release alpha` → `ldm install` → gateway restart.

### Step 4. Phase 4 — Gateway.log emergency ingestion (Layer 2)

- **What:** Last-resort ingestion: parse `~/.openclaw/logs/gateway.log` for assistant text that never made it into a session JSONL. Lower confidence, tagged `source_type: "gateway-log"`.
- **Files:** new `src/gateway-log-ingest.ts` + dedup-by-hash against existing crystal chunks.
- **Risk:** contained. Unstructured log parsing uses heuristics; chunks get lower weight.
- **Ship:** same flow as Step 3.

Layer-1 phases (OpenClaw fork changes — higher risk, `openclaw doctor` gate mandatory):

### Step 5. Phase 1 — Flush before session rotate (Layer 1)

- **What:** OC emits a hook `beforeSessionRotation(oldSessionId)` before abandoning a session. Memory-crystal consumes it and runs a final ingestion pass with `force: true`.
- **Files:** `src/agents/session-*.ts` in OC fork (find the rotation site) + new hook dispatch. Consumer in `memory-crystal-private/src/openclaw.ts`.
- **Risk:** OC core surgery. Patch Tracking row in `UPGRADE-RUNBOOK.md`. `openclaw doctor` must pass post-build.
- **Ship:** commit to `cc-mini/chat-completions-v2026.4.11`, rebuild, `openclaw doctor` → `npm link` → verify. Add Patch Tracking row. Also ship consumer as new memory-crystal alpha.
- **Consider upstream PR:** this is a generally useful hook; file to `openclaw/openclaw` after it proves out locally.

### Step 6. Phase 3 — Partial turn ingestion (Layer 1)

- **What:** `agent_end` fires only on success. Add `agent_error` (or make `agent_end` fire on failure too) so partial turns are ingested with `partial: true` tag.
- **Files:** `src/agents/agent-runner-*.ts` in OC fork + consumer in memory-crystal.
- **Risk:** OC agent runner change. Same doctor gate.
- **Ship:** same flow as Step 5.

### Step 7. Phase 6b — Cross-provider tool_use ID normalization (Layer 1)

- **What:** Normalize Grok composite IDs (`call-xxx|fc_zzz`) to Anthropic-compatible alphanumeric at serialization so fallback to Anthropic doesn't break validation.
- **Files:** `src/agents/pi-embedded-runner/*.ts` in OC fork (the message serializer layer).
- **Risk:** Touches the serializer; affects every model that flows through it. Test with Grok + Anthropic specifically. **Doctor gate.**
- **Ship:** same flow as Step 5. Upstream PR is a priority here (benefits every OC user with multi-provider fallback).

### Step 8. Phase 6c — Session rotation threshold (Layer 1)

- **What:** Raise the failure threshold before OpenClaw abandons a session. Try repair (truncate the corrupt turn) before rotation. The manual truncation at line 4887 on Apr 11 worked; automate it.
- **Files:** OC session lifecycle code.
- **Risk:** Highest risk of all phases — wrong logic could loop on a corrupt turn forever. Needs careful bounds (max N repair attempts before rotating anyway).
- **Ship:** same flow. **Gate on unit test** (simulate corrupt turn, assert repair attempt count and rotation fallback).

### Step 9. Phase 6a — OpenClaw format-error billing cooldown (Layer 1)

Held pending investigation (see Step 2 above). After Step 2's bug report update, decide whether to:
- Patch the classifier with a confirmed repro, OR
- Close the bug as "not-a-bug" (credits genuinely ran out), OR
- Add Phase 6a back into Step 5-8's sequence with a real fix design.

## Recommended execution order

Everything Layer-2 first (Steps 1, 3, 4). All Layer-1 changes come after we stabilize memory-crystal + have Phase 6a evidence resolved:

1. **Now:** Step 1/1b (Phase 5 ship+install — alpha dogfood)
2. **Now:** Step 2 (bug report update for Phase 6a)
3. **Next session:** Step 3 (chat.db fallback) + Step 4 (gateway.log ingest)
4. **After:** Step 5 + Step 6 (Layer 1 hooks — flush, partial turn)
5. **After:** Step 7 (tool_use ID normalization — consider upstream PR)
6. **Last:** Step 8 (session rotation threshold — highest-risk change)

## Decision points for Parker

1. **Go on Step 1 + 1b** (publish alpha → `ldm install` → gateway restart → verify). Alpha dogfood loop, reversible via rollback to alpha.4.
2. **Go on Step 2** (hold Phase 6a, update bug report with log evidence). Alternative: want me to dig into the gateway logs myself for a confirmed repro before calling it a phantom, or patch speculatively anyway?
3. **Scope for this session:** ship Steps 1+2 only (my default), OR push through Steps 3+4 (Layer-2, also low risk) too, OR tackle one Layer-1 phase now as well?
