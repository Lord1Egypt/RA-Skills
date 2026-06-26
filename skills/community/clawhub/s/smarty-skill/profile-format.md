# Profile Format — Smarty Skills-Infra

Rewrite `memory/context-infra/context-profile.md` entirely during each reflection.

## Structure

```markdown
# User Context Profile

## Axioms
Sorted by strength (highest first). Apply as soft defaults.

- I prefer [specific preference].
  strength: N | domain: [domain] | last-confirmed: YYYY-MM-DD

## Patterns (Not Yet Axioms)
Below the 3-context promotion threshold.
- [Emerging pattern] (N contexts, domain: [domain])

## Dormant
Unconfirmed 30+ days. Not applied as defaults. Prune after 90 days.
- *[Axiom]* — strength: N, domain: [domain], last-confirmed: YYYY-MM-DD

## Contradictions
Do not apply until resolved by future observations.
- [Axiom]
  Conflict: [description] (YYYY-MM-DD)
```

## Writing Rules
- First person: "I prefer..." / "I want..." / "I value..."
- One sentence. Specific enough that two engineers apply it identically. "I like clean code" is too vague. "I prefer early returns over nested if-else" is actionable.
- Strength starts at supporting observation count (minimum 3). Increment on reinforcement.
- When approaching 25-axiom cap, merge related axioms over dropping them.
