---
name: restart-task-recovery
description: Preserve and resume in-progress multi-agent work across OpenClaw config patch/apply restarts. Use when a restart is required during active tasks, when users ask to minimize interruption, or when agent runs/tool calls were interrupted by gateway restart/timeouts.
---

# Restart Task Recovery

Use this workflow to maximize successful recovery after OpenClaw restart.

## 1) Pre-restart checkpoint (required)

Before any `gateway.config.patch`, `gateway.config.apply`, `gateway.update.run`, or `gateway.restart`:

1. List active sessions that may be impacted (`sessions_list`).
2. For each active work session, capture the latest context (`sessions_history`, limit 20-50).
3. Write a compact checkpoint file at:
   - `memory/restart-checkpoints/<YYYY-MM-DD>/<HHmmss>.md`
4. Include per session:
   - sessionKey / label / agent
   - goal
   - last completed step
   - next exact step
   - blocked dependencies (if any)
   - a ready-to-send resume message (1-2 lines)

Keep checkpoint concise and executable.

## 2) Restart with explicit recovery intent

When calling gateway restart/config change, set `note` to include recovery intent, e.g.:
- “配置已更新并重启；将按 checkpoint 恢复中断任务。”

## 3) Post-restart recovery sweep

After restart:

1. Re-list sessions (`sessions_list`) and compare against checkpoint.
2. For each interrupted/idle target session, send resume message via `sessions_send`:
   - “Continue where you left off. Last completed: <x>. Next: <y>. If previous tool call failed, retry from <y>.”
3. Do **not** poll in tight loops. Check on-demand only.
4. Summarize recovery status to user:
   - recovered sessions
   - still blocked sessions
   - manual follow-up needed

## 4) Idempotent task design rules

When resuming tasks, enforce:

1. Re-run-safe steps (idempotency key / upsert / duplicate-safe writes).
2. Small step boundaries with explicit “done markers”.
3. External writes batched, not one-by-one loops.
4. On uncertainty, verify state first then continue.

## 5) V2 automation helper

Use script: `scripts/build_checkpoint.py` to generate checkpoint markdown from structured JSON.

Example:

```bash
cat session-snapshot.json | python3 scripts/build_checkpoint.py memory/restart-checkpoints/$(date +%F)/$(date +%H%M%S).md
```

Expected stdin JSON shape:

```json
{
  "sessions": [
    {
      "sessionKey": "agent:engineer:main",
      "agentId": "engineer",
      "goal": "Finish regression verification",
      "lastDone": "401/幂等/时区/retention case passed",
      "nextStep": "Publish final acceptance summary",
      "blockers": "none"
    }
  ]
}
```

## 6) V3 resume-plan automation

Use script: `scripts/generate_resume_plan.py` to parse the latest checkpoint and produce a structured resume plan.

Example:

```bash
python3 scripts/generate_resume_plan.py memory/restart-checkpoints/2026-03-09/162200.md /tmp/resume-plan.json
```

Then send each `items[].resumeMessage` to `items[].sessionKey` via `sessions_send`.

Rules:
- Send once per session (no loop polling).
- If a session is already active and progressing, skip resend.
- After sends, post one concise recovery summary to user.

## 7) V4 one-click recovery payload generator

Use script: `scripts/recover_from_latest_checkpoint.py`.

It auto-selects the latest checkpoint file and emits a ready JSON payload list for `sessions_send` calls.

Examples:

```bash
# Use latest checkpoint automatically
python3 scripts/recover_from_latest_checkpoint.py > /tmp/recover-actions.json

# Use a specific checkpoint
python3 scripts/recover_from_latest_checkpoint.py memory/restart-checkpoints/2026-03-09/162200.md > /tmp/recover-actions.json
```

Execution guidance:
- Read `/tmp/recover-actions.json`
- Execute each `actions[]` item with `sessions_send`
- Post one concise summary to user

## 8) V5 pre-resume verifier + manual confirmation gate

Use script: `scripts/pre_resume_verify.py` to score resume actions before sending.

Examples:

```bash
python3 scripts/pre_resume_verify.py /tmp/recover-actions.json /tmp/recover-verified.json
```

Behavior:
- Marks each action as `risk=normal|high`
- `high` risk actions are set to `decision=hold` and `requiresManualConfirm=true`
- Only send `decision=send` automatically
- Ask user confirmation before executing held actions

Recommended execution flow:
1. Generate actions with V4
2. Verify with V5
3. Send all `decision=send`
4. Present `decision=hold` list to user for explicit confirmation

## 9) V6 execution-plan generator (auto-send safe items)

Use script: `scripts/execute_verified_recovery.py` with V5 output.

Example:

```bash
python3 scripts/execute_verified_recovery.py /tmp/recover-verified.json > /tmp/recover-exec.json
```

Behavior:
- Emits `sendActions[]` for auto-safe resumes (`decision=send`)
- Emits `holdForManualConfirm[]` for risky resumes (`decision=hold`)

Execution:
1. Execute all `sendActions[]` with `sessions_send`
2. Ask user to confirm `holdForManualConfirm[]`
3. Execute confirmed held items
4. Post concise summary

## 10) Message templates

Read and use: `references/templates.md`
