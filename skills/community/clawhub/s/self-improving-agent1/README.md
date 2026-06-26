# 🧠 Learning Capture

**Remember mistakes without turning your agent into a chaos monkey.**

This skill captures corrections, failed tool runs, recurring gotchas, and useful project lessons as short markdown notes in `.learnings/`.

It is intentionally conservative:

- no raw transcripts
- no credentials or auth tokens
- no automatic rule changes
- no hooks required
- durable instruction changes require explicit user approval

## What It Does

- Logs user corrections as reusable learnings
- Logs unexpected tool/command failures with redacted evidence
- Tracks missing capabilities as feature requests
- Links recurring issues so patterns become visible
- Proposes durable rules only after enough signal exists

## Files

```text
.learnings/
├── LEARNINGS.md
├── ERRORS.md
└── FEATURE_REQUESTS.md
```

## Example

```markdown
## LRN-20260507-001 — check-existing-skill-slug

**Priority:** medium
**Status:** pending
**Area:** workflow

### Summary
Before publishing a ClawHub skill, inspect the exact slug first.

### Better next time
Run `clawhub inspect <slug>` and verify owner/latest status before publishing.
```

## Not For

- storing secrets
- copying private chat logs
- editing system/agent instructions without approval
- automatic self-modification

---

*by brasco05 · conservative learning capture for AI-assisted work*
