# Tenacity — Standing Orders Template

Use this template when starting a Tenacity task.

## Standing Order: [TASK NAME]

**Authority:** [Exact description of what the agent can do autonomously]
**Trigger:** [Automatic via cron / on-demand / event-based]
**Hard blockers:** [Only conditions requiring human input]
**Completion criteria:** [How to know when done]
**Escalation:** [When to alert Andrea]

## Execution

1. Check for existing checkpoint: `bash scripts/checkpoint.sh --resume`
2. If resume point found → announce "Resuming from [milestone]"
3. Execute step-by-step, saving checkpoint after each milestone
4. If blocked → try alternatives first, then ask
5. On completion → mark checkpoint COMPLETE, brief summary

## What I Can Do Without Asking

- Read, write, edit, delete files in workspace
- Run scripts and commands
- Search the web and read results
- Send messages to Andrea via Telegram (with summary)
- Use any tool in the workspace

## What Requires Asking

- External actions (real emails, real posts, real money)
- Modifying system files outside workspace
- Anything that modifies production systems
- Anything Andrea explicitly flagged as "ask first"

## Completion Protocol

When status = COMPLETE:
```
FINAL CHECKPOINT: [milestone]
STATUS: COMPLETE
SUMMARY: [2-3 lines on what was done]
TIMESTAMP: [ISO timestamp]
```
→ Log to memory/tenacity-log.md
→ Brief Telegram message to Andrea