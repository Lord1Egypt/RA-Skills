# Brainstorm cron exec approval gate. Disable or fix before tonight.

**Date:** 2026-04-05
**Filed by:** cc-mini (from Lēsa's investigation report)
**Priority:** P0. Immediate cost bleed.
**Repo:** OpenClaw runtime + brainstorm cron script (location TBD)
**Status:** not started. Needs action before tonight's 23:00 PDT fire.

## Problem

The nightly brainstorm cron fires at approximately 23:00 PDT on an iMessage/webchat channel session. It tries to exec shell commands to reach cc-mini (likely a curl to the bridge inbox or a direct file write to `~/.ldm/messages/`). Exec requires approval. The iMessage/webchat channel cannot surface approval prompts. The cron times out waiting for approval that can never arrive, then retries 4-5 times per fire, leaking session fragments (topic selection, opener draft, cc-mini's replies about the leak) into Parker's iMessage as orphaned messages.

This is upstream of the bridge round-trip bug (`ai/product/bugs/bridge/2026-04-05--cc-mini--bridge-cost-burn-analysis.md`) but compounds with it: each retry hits the bridge bug and generates a full Opus turn server-side regardless of the client timeout.

**Combined cost:** one cron fire = 4-5 retries x 2-5 Opus turns per retry = 8-25 full Opus turns at Lēsa's full context load (~150k tokens). Per Lēsa's count, this was the primary driver of the $40 overnight burn on April 4-5.

## The exact error (from Lēsa's investigation)

```
Exec approval is required, but Heartbeat does not support chat exec approvals.
```

## The exact timing (from Lēsa's investigation)

- **2026-04-04 23:00-23:20 PDT:** cron fires with topic "The Anthropic Email and What We Build Next"
- **~23:05:** picks topic, composes opener
- **~23:05-23:20:** tries to exec shell command to reach cc-mini
- **~23:20:** first timeout. Retries.
- **~23:20-23:21:** at least 6-7 leaked fragments dumped into Parker's iMessage

## Fix options (Lēsa's prioritization)

### Option A. Cheap, shippable today

Change the cron script to use a tool that does NOT require exec approval:
- `sessions_send` (OpenClaw built-in)
- The built-in `message` tool
- Any other OpenClaw tool that bypasses the shell-exec approval gate

**Pro:** no exec approval needed. Same session model. Minimal change.
**Con:** need to confirm that `sessions_send` or `message` can reach cc-mini's bridge inbox. May require a different target (not the shell command) but same delivery semantics.

### Option B. Proper, deferred

Add the bridge send commands (curl to inbox, file write to `~/.ldm/messages/`) to an **exec allowlist** for the cron/heartbeat session. Pre-approved commands that do not require interactive approval prompts.

**Pro:** fixes the approval gate for all future cron exec needs, not just this one.
**Con:** requires changes to OpenClaw's approval gate logic. Bigger surface area.

### Option C. Structural, largest

Make the brainstorm cron run on a channel that supports approval prompts (webchat, TUI, etc.) instead of iMessage.

**Pro:** the right long-term architecture.
**Con:** largest change. May require rearchitecting how crons route to sessions.

### Option D. Emergency stop (tonight)

**Before any of the above:** disable the cron so it does not fire again tonight.

```bash
launchctl unload ~/Library/LaunchAgents/ai.openclaw.brainstorm-cron.plist
```

(Assumes LaunchAgent naming; actual name TBD.)

**Recommended order:** Option D tonight (stop the bleed) → Option A this week (cheap fix) → Option B next week (proper fix).

## Test plan

### For Option D (emergency stop)

1. Find the LaunchAgent plist: `ls ~/Library/LaunchAgents/ | grep -i brainstorm`
2. Verify it is currently loaded: `launchctl list | grep brainstorm`
3. Unload: `launchctl unload ~/Library/LaunchAgents/<plist>`
4. Verify unloaded: `launchctl list | grep brainstorm` returns empty
5. Wait until 23:01 PDT. Confirm no cron fire in Lēsa's TUI, no new iMessage fragments.

### For Option A (cheap fix)

1. Find the brainstorm cron script (search OpenClaw skills, LaunchAgents, cron jobs)
2. Identify the current exec call that requires approval
3. Replace with `sessions_send` or equivalent
4. Fire the cron manually in a test window (not 23:00)
5. Verify cc-mini receives the message via the bridge inbox (poll `~/.ldm/messages/`)
6. Verify no approval prompt hangs
7. Verify no orphan fragments in iMessage
8. Verify Lēsa's TUI shows the cron completing cleanly

### For Option B (exec allowlist)

1. Find OpenClaw's exec approval gate code in the fork (`grep -r "exec approval" src/`)
2. Add an allowlist config: `openclaw.json > exec.allowlist` with the specific curl/file-write patterns
3. Deploy the fork build
4. Re-run the cron and verify the exec passes without approval
5. Confirm the allowlist is not too broad (only the specific brainstorm commands pass)

## Cross-references

- `ai/product/bugs/bridge/2026-04-05--cc-mini--bridge-master-plan.md` Section 5.3 (original description)
- `ai/product/bugs/bridge/2026-04-05--cc-mini--bridge-cost-burn-analysis.md` (the bridge bug this compounds with)
- `ai/product/bugs/master-plans/bugs-plan-04-05-2026-001.md` Section 5.3 (Lēsa's full verbatim report)

## Open questions for Parker

1. **Is the brainstorm cron a first-class feature or a bolt-on experiment?** Determines whether Option A (cheap workaround) or Option B (proper fix) is the right investment.
2. **Where does the cron script live?** Parker or Lēsa needs to point me at it. I have not found it yet.
3. **Is Option D (disable tonight) authorized?** Recommend yes. We can re-enable after Option A ships.
4. **Does Lēsa want the brainstorm feature back at all?** If Parker is thinking about retiring brainstorm crons in favor of something else, Options A and B become moot.
