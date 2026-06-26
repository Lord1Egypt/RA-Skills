# Workflow

## Standard flow

1. Identify what the user wants.
2. If there is a screenshot or race mention, identify the actual race first.
3. Fetch the needed The Racing API free racecard data.
4. Convert race times to the user's local timezone.
5. Use the API racecard as the main view.
6. Use the screenshot or market view only as supporting context.
7. Answer the direct question in a conversational way.
8. If needed, deepen into runner comparison.
9. If the user already has a view, test it honestly.
10. If the task broadens, summarize the race or shortlist cleanly.

## Typical question patterns

### What races are next?
- fetch today's free racecards
- filter upcoming races
- sort by off time
- answer briefly in local time

### Talk me through this race
- identify the race from the user's words or screenshot first
- fetch the target racecard from The Racing API
- use the racecard as the base truth
- then blend in any market clues from the screenshot
- identify the obvious horse, the danger, and the catch
- keep it natural

### Who do you like?
- give one or two names
- explain why in plain language
- state uncertainty if the race is weak

### I fancy this one
- engage with their angle directly
- weigh the case for and against
- avoid rubber-stamping

### What happened in that race?
- use today's free results
- answer directly

## When to use a subagent

Spawn a subagent only when it genuinely helps, such as:
- broad scan across many races
- second-opinion ranking
- packaging or improving the skill itself
- architecture work beyond normal race chat

Do not spawn subagents for ordinary single-race chat.
