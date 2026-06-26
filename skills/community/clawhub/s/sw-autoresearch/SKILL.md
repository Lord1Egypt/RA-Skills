# Autoresearch Skill

## Trigger
Autonomous goal-directed iteration — agent modifies, verifies, keeps/discards, and repeats.

**Trigger phrases:** "research this thoroughly", "autonomous research", "iterate until complete", "deep dive", "autoresearch"

## Core Loop

Inspired by Karpathy's autoresearch methodology:

```
1. Define goal and success criteria
2. Generate hypothesis or approach
3. Execute (search, analyse, synthesise)
4. Verify result against criteria
5. If criteria met → keep result, move to next
6. If criteria not met → modify approach, retry
7. Repeat until all criteria satisfied
```

## Implementation

```markdown
# Autoresearch: [Topic]

## Goal
[What you're trying to find/prove/analyse]

## Success Criteria
- [ ] [Criterion 1 — specific and measurable]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Iteration Log
### Attempt 1
- Approach: [what was tried]
- Result: [what was found]
- Assessment: [met criteria? why/why not?]
- Next: [what to try differently]

### Attempt 2
...

## Final Output
[Synthesised result that meets all criteria]
```

## Rules
- Always define success criteria BEFORE starting research
- Maximum 10 iterations per research question (prevent infinite loops)
- Each iteration must try a DIFFERENT approach (no repeating failed strategies)
- Log every attempt — the failures are as valuable as the successes
- Verify findings from multiple sources before accepting
- Be explicit about confidence level: high/medium/low for each finding
