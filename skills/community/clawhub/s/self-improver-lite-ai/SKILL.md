---
name: self-improver-lite
description: Runs lightweight self-audits of OpenClaw behavior, finds repeated failures, proposes safe config/process improvements, and tracks what changed. Use after incidents, silent-bot periods, rate-limit spikes, or weekly maintenance.
---

# Self Improver Lite

## Goal

Continuously improve reliability without risky autonomous changes.

## Trigger Cases

- Bot is silent or unstable
- Same error appears repeatedly (`rate_limit`, `orphaned`, `timeout`, `sendMessage failed`)
- After major config updates
- Scheduled weekly health review

## Audit Steps

1. Collect evidence:
```bash
systemctl is-active openclaw-gateway ollama
journalctl -u openclaw-gateway -n 120 --no-pager
```
2. Group failures by pattern and count.
3. Identify top 1-3 root causes.
4. Propose minimal, reversible fixes.
5. Apply only low-risk fixes automatically.
6. Record summary and next actions.

## Auto-Allowed Changes

- Session cleanup when `orphaned user message` loops
- Gateway restart for stuck polling
- Context window/maxTokens tuning within known-safe ranges
- Fallback chain reordering (no key changes)

## Requires Explicit User Approval

- New API provider onboarding
- Social network account actions
- Financial/crypto operations
- Credential rotation or deletion
- Any destructive file cleanup beyond sessions/log rotation

## Weekly Review Template

```markdown
## Weekly Self-Audit
- Period: <dates>
- Uptime notes: <short>

### Top Errors
1. <error> — <count>
2. <error> — <count>

### Changes Applied
- <change 1>
- <change 2>

### Measured Impact
- Response latency: <before -> after>
- Failed runs: <before -> after>

### Next Improvements
- <single highest-impact next step>
```

## Guardrails

- Never expose secrets in reports.
- Always keep a rollback path (backup old config before edits).
- Prefer one change per cycle to keep causality clear.
