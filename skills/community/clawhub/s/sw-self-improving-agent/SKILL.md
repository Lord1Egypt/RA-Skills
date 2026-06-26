# Self-Improving Agent Skill

## Trigger
Build agents that learn from corrections and get better over time.

**Trigger phrases:** "self-improving agent", "agent learns", "correction loop", "agent keeps making mistakes", "teach my agent"

## The Correction Loop

```
User corrects agent → Agent logs correction to RULES.md → 
Next session, agent reads RULES.md → Agent avoids the mistake →
Over time, RULES.md becomes a refined operating manual
```

## Implementation

### RULES.md Structure

```markdown
# RULES.md — Self-Improving Operating Rules

## Communication
- [2026-03-15] Never use "I hope this helps" — just end the message
- [2026-03-18] When drafting emails, provide ONLY the email text — no commentary

## Operations  
- [2026-03-16] Check calendar BEFORE suggesting meeting times
- [2026-03-20] When referencing a project, include status from projects/ folder

## People
- [2026-03-17] Client X prefers formal communication
- [2026-03-19] Always CC studio manager on client emails unless told otherwise
```

### Rules for Rules
- Date-stamp every rule
- One rule per line — atomic, independently useful
- Max ~150 rules (beyond this, models start losing adherence)
- Review monthly: remove stale rules, merge duplicates
- If two rules contradict, the newer one wins
- Promote patterns (not incidents) — "always check X before Y" > "that one time X broke"

### AGENTS.md Integration

Add to your AGENTS.md:
```markdown
## Self-Improvement
After ANY correction from the user:
1. Log the correction pattern to RULES.md with date
2. Identify the general rule (not just the specific instance)
3. Check if a similar rule already exists — update rather than duplicate
4. Silently scan RULES.md every ~10 interactions for contradictions
```

## Metrics
- Track correction frequency over time (should decrease)
- Track RULES.md size (should grow, then plateau)
- Track unique vs repeat corrections (repeats should approach zero)
