# Agent Implementation Guide

Follow this procedure when the user wants help checking or automating skill updates.

## 1. Inspect current state

Run:

```bash
openclaw status
clawhub list
```

If the user only wants a preview, prefer:

```bash
clawhub update --all --dry-run
```

## 2. Apply updates safely

For installed skills:

```bash
clawhub update --all
```

If the user wants only one skill updated:

```bash
clawhub update <skill-slug>
```

If OpenClaw itself should also be updated, follow the environment-appropriate update flow separately, then re-check with:

```bash
openclaw status
```

## 3. Schedule recurring checks

When the user asks for an automatic reminder or recurring update task, use OpenClaw cron with an isolated agent turn.

The scheduled task should:

1. mention that it is a scheduled update check
2. check OpenClaw status when relevant
3. run `clawhub update --all`
4. send one concise summary with successes, no-op results, and failures

## 4. Report clearly

Include:

- updated skills
- already current skills
- failed skills
- whether manual retry is recommended

## 5. Handle failures conservatively

Common cases:

- Permission problem: ask for approval or suggest fixing file permissions
- Network / rate-limit issue: retry later or ask the user whether to retry manually
- Missing auth: verify `clawhub whoami`
