# Pattern Harvesting Guide

## When to harvest a learning
Harvest into `.learnings/` when:
- the user corrects the agent
- a command/tool fails and you fix it
- a workaround becomes reliable
- a better generic strategy is found
- a repeated attempt reveals a stable path

## Good learning pattern
A useful learning should answer:
- what happened
- what failed or was missing
- what eventually worked
- what rule can be reused later

## Recommended structure
- Summary
- Trigger
- Failure or friction
- Resolution
- Reusable rule
- Suggested action

## Bad learning pattern
Avoid entries that are only:
- raw logs
- one-off trivia with no reuse value
- sensitive secrets or credentials
- vague statements like “be careful next time”

## Promotion heuristic
If a learning is reused repeatedly or keeps proving true, consider promoting it into durable memory.
