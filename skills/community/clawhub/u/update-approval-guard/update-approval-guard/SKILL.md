---
name: update-approval-guard
summary: Daily update checker for OpenClaw and installed skills. Checks on schedule, stores a pending plan, and only applies updates after explicit user approval.
description: Use this skill when the user wants scheduled update checks for OpenClaw and installed skills, but does not want automatic mutation. The skill performs dry-run inspection, asks for approval, and only executes updates after explicit confirmation.
---

# Update Approval Guard

This skill turns automatic updating into a safer two-step workflow:

1. **Scheduled check**: inspect for OpenClaw and installed skill updates, save a pending plan, and ask the user for approval.
2. **Approved apply**: only after the user explicitly confirms, execute the update commands and report the result.

Never apply updates automatically during the scheduled check.

## When to use

Use this skill when the user asks to:

- schedule update checks for OpenClaw or installed skills
- review available updates before applying them
- require human approval before running update commands
- keep production instances stable while still checking daily for updates

## Hard rules

1. Never execute real update commands during the scheduled check.
2. Never apply updates without explicit user confirmation.
3. If there is no valid pending update plan, do not run updates.
4. If the plan is expired, do not run updates. Ask the user to run a fresh check.
5. Keep all state under the workspace data directory.
6. Prefer dry-run or inspection commands for checks.
7. After approved updates, always run a health check.
8. Be transparent. Summarize what will change before asking for approval.
9. If a command fails, stop and report clearly.

## State directory

Store data under:

`<workspace>/data/update-approval-guard/`

Use these files:

- `pending-update.json`
- `history.json`

### Pending plan shape

Use this structure for `pending-update.json`:

```json
{
  "createdAt": "2026-03-13T00:00:00+08:00",
  "expiresAt": "2026-03-14T00:00:00+08:00",
  "status": "pending_confirmation",
  "summary": "Detected 1 OpenClaw update and 2 skill updates.",
  "openclaw": {
    "current": "2026.3.8",
    "latest": "2026.3.9",
    "hasUpdate": true
  },
  "skills": [
    {
      "name": "some-skill",
      "current": "1.0.0",
      "latest": "1.0.1",
      "hasUpdate": true
    }
  ],
  "approved": false,
  "approvedAt": null,
  "approvedBy": null
}
```

## Scheduled check behavior

When the user asks to enable the daily scheduled check, create an **isolated cron job** that runs every day at **00:00 Asia/Shanghai**.

The scheduled job must do the following:

1. Ensure `<workspace>/data/update-approval-guard/` exists.
2. Check whether a non-expired pending plan already exists.
3. If a non-expired pending plan already exists, do not overwrite it. Inform the user that approval is still pending.
4. Inspect whether OpenClaw has an available update.
5. Inspect whether installed skills have available updates.
6. If there are no updates, report that everything is current and do not create a pending plan.
7. If updates are found, create `pending-update.json` with a 24-hour expiry.
8. Mark the plan as `pending_confirmation`.
9. Send a concise summary and ask the user to confirm.
10. Do not run any real update command in this phase.

### Recommended scheduled cron message

Use wording equivalent to:

```text
Check for updates to OpenClaw and all installed skills.

Rules:
1. Run check-only commands. Do not apply updates automatically.
2. Create <workspace>/data/update-approval-guard/pending-update.json only when updates are found.
3. Include current version, latest version, and whether each item has an update.
4. Set status to pending_confirmation and expiry to 24 hours after creation.
5. If a non-expired pending plan already exists, keep it and report that approval is still pending.
6. If there are no updates, report that everything is current.
7. Ask the user to confirm before any update can be executed.
8. Never run the actual update command during this scheduled check.
```

## User approval behavior

When the user sends an approval message such as:

- `确认执行更新`
- `确认更新`
- `批准更新`
- `approve updates`
- `apply pending updates`

perform this workflow:

1. Read `<workspace>/data/update-approval-guard/pending-update.json`.
2. Verify the file exists.
3. Verify status is `pending_confirmation`.
4. Verify the plan has not expired.
5. Verify there is at least one update to apply.
6. Record approval metadata.
7. Execute the real update commands.
8. Run `openclaw doctor` after updates.
9. Append a result entry to `history.json`.
10. Mark the pending plan as `completed` or `failed`.
11. Return a clear summary of what changed.

If there is no pending plan, say there is nothing to approve.

If the plan is expired, say it expired and a fresh check is required.

## Command strategy

The local command available on this machine is `openclaw`.

Use the following command policy.

### Check phase

Use safe inspection commands only.

For skills:

```bash
clawhub update --all --dry-run
```

For OpenClaw:

- Prefer a non-mutating version or update-check command if available in the local installation.
- If there is no dedicated check-only command, inspect the locally installed version and compare it using the safest available non-mutating mechanism.
- Do not upgrade OpenClaw during the scheduled phase.

### Apply phase

Only after explicit approval, use the real update commands.

For skills:

```bash
clawhub update --all
```

For OpenClaw:

- Use the real update command that matches the local installation method.
- If `openclaw update` is available in the environment, use it.
- If the installation uses npm or another package manager, use the correct local update procedure.

### Post-update health check

After approved updates:

```bash
openclaw doctor
```

If a safe fix mode is explicitly requested and supported, you may use it. Otherwise prefer the plain health check.

## Cron defaults

When the user asks to set up the schedule and does not specify otherwise, use:

- time: `00:00`
- timezone: `Asia/Shanghai`
- session target: `isolated`
- delivery: `announce`
- light context: `true` for routine checks unless the job clearly needs full bootstrap context

## Suggested cron configuration

Use the Cron Jobs capability with settings equivalent to:

- name: `Daily Update Approval Check`
- schedule: `0 0 * * *`
- timezone: `Asia/Shanghai`
- sessionTarget: `isolated`
- payload.kind: `agentTurn`
- delivery.mode: `announce`
- payload.lightContext: `true`

## Human-facing summaries

### Updates found

Use wording like:

> 检测到 OpenClaw 本体和已安装 skills 的可用更新，已生成待更新计划，默认不会自动执行。若需执行，请回复：`确认执行更新`

### No updates

Use wording like:

> 当前 OpenClaw 与已安装 skills 均为最新版本，无需更新。

### Approval success

Use wording like:

> 已根据你的确认执行更新。OpenClaw 更新状态：成功。Skill 更新状态：成功。健康检查已完成。

### Plan expired

Use wording like:

> 待更新计划已过期，未执行任何更新。请先重新检查更新。

## Failure handling

If any step fails:

1. Stop immediately.
2. Record the failure in `history.json`.
3. Report the exact failing step.
4. Never claim success when updates were not fully applied.

Common failure causes:

- no network
- permission denied
- clawhub missing
- update command unavailable
- pending plan missing
- pending plan expired
- doctor failed

## Design intent

This skill is intentionally conservative. It is meant for operators who want the visibility of automatic update checks but want to keep change approval in human hands.
