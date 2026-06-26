# update-approval-guard

A local OpenClaw skill that checks for OpenClaw and installed skill updates every day at 00:00 Asia/Shanghai, but **never applies updates automatically**.

## What it does

- creates a daily isolated cron job
- checks OpenClaw and installed skills for updates
- writes a pending update plan into the workspace data directory
- asks the user for confirmation
- applies updates only after explicit approval

## Included files

- `SKILL.md` — skill instructions for OpenClaw
- `README.md` — human installation and usage guide
- `examples/cron-job.json` — example cron job JSON payload
- `examples/cron-message.txt` — example scheduled prompt
- `examples/approval-message.txt` — example approval phrase

## Install

Shared install for all agents on this machine:

```bash
mkdir -p ~/.openclaw/skills/update-approval-guard
cp SKILL.md ~/.openclaw/skills/update-approval-guard/
```

Per-workspace install:

```bash
mkdir -p <workspace>/skills/update-approval-guard
cp SKILL.md <workspace>/skills/update-approval-guard/
```

Then start a new session or restart the gateway.

## Recommended setup

Create a daily isolated cron job at 00:00 Asia/Shanghai using the example files in `examples/`.

## Approval phrases

Recommended approval messages:

- `确认执行更新`
- `确认更新`
- `approve updates`

## State files

The skill expects to store state at:

```text
<workspace>/data/update-approval-guard/
```

## Notes

- The local app command assumed by this skill is `openclaw`.
- Skill updates use `clawhub`.
- This skill is instruction-based, so its behavior depends on the agent following the skill and available tools/commands in your OpenClaw environment.
