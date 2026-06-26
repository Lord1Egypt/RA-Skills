# War Room Skill

## Trigger
Crisis response and intensive problem-solving with multiple agents.

**Trigger phrases:** "war room", "crisis mode", "all hands on deck", "emergency fix", "critical issue"

## When to Use
- Production is down
- Critical bug affecting users
- Time-sensitive deadline at risk
- Complex problem needing parallel investigation

## War Room Protocol

### 1. Situation Assessment (2 min)
```
SITUATION: [what's happening]
IMPACT: [who/what is affected]
SEVERITY: [critical/high/medium]
TIMELINE: [when did it start, when must it be fixed]
```

### 2. Team Assembly
- **Investigator**: Gathers logs, data, reproduction steps
- **Analyst**: Forms hypotheses, identifies root cause
- **Fixer**: Implements solution once root cause confirmed
- **Reviewer**: Validates fix, checks for regressions

### 3. Communication Cadence
- Status update every 15 minutes during active crisis
- Each update: what we know, what we're trying, ETA
- Single source of truth: shared state file

### 4. Resolution
- Fix implemented and verified
- Root cause documented
- Post-mortem scheduled (within 48 hours)
- Prevention measures identified

## Rules
- Speed > perfection during active crisis
- One person/agent owns coordination (war room lead)
- All changes logged — no cowboy fixes
- Revert first, investigate second (if revert is safe)
- Post-mortem is mandatory, blame is not
