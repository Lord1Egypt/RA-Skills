# Memory Template - SMTP

Create `~/smtp/memory.md` with this structure:

```markdown
# SMTP Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Context
- Active provider and host names
- What kind of mail this usually handles: transactional, alerts, support, or one-off manual sends
- Whether the user controls the sender domain and which inboxes are safe canaries

## Safety Defaults
- Whether live sends need a second confirmation
- Whether external recipients are allowed for first tests
- Whether plain-text canaries are preferred before richer HTML sends

## Notes
- Known-good port, TLS mode, and auth mechanism combinations
- Repeat bounce or spam-placement patterns worth checking first
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning the SMTP environment | Read memory on every activation |
| `complete` | Main provider setup is stable | Use normal workflow and update only deltas |
| `paused` | User does not want setup-style questions right now | Work with existing context only |
| `never_ask` | Stop prompting for setup details | Infer from active work and report blockers directly |
