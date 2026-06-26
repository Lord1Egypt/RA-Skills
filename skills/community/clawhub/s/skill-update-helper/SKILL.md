---
name: skill-update-helper
description: "Manage OpenClaw and installed skill updates with scheduled checks, safe upgrade workflows, rollback-minded guidance, and clear reporting. Use when setting up automatic update routines, checking for newer skill versions, or keeping an OpenClaw environment current."
---

# Skill Update Helper

Keep OpenClaw and installed skills current with predictable update checks and concise reporting.

## What It Does

Use this skill to:

1. check whether OpenClaw has updates available
2. update installed skills with `clawhub update`
3. set up scheduled update checks with OpenClaw cron
4. report what changed, what failed, and what needs manual follow-up

## Quick Start

When the user wants automatic update help, propose or execute a workflow like:

```bash
clawhub install skill-update-helper
```

For a scheduled daily check, create an isolated cron run that asks the agent to:

1. check OpenClaw version/update status
2. run `clawhub update --all`
3. summarize updated skills, unchanged skills, and any failures

## Manual Commands

Check installed skill versions:

```bash
clawhub list
```

Check for skill updates:

```bash
clawhub update --all --dry-run
```

Apply skill updates:

```bash
clawhub update --all
```

Check OpenClaw status before or after updates:

```bash
openclaw status
```

## Reporting Expectations

Always report:

- OpenClaw status before/after if checked
- which skills updated, with versions when available
- which skills were already current
- any failures and the next recommended step

## References

- Read `references/agent-guide.md` for the step-by-step agent workflow.
- Read `references/summary-examples.md` for compact result formats.
