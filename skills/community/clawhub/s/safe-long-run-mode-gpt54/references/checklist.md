# GPT-5.4 Only Long-Run Checklist

## Pre-flight

Before starting:
1. What is the deliverable?
2. What files will be created or edited?
3. Which external systems may throttle?
4. Should this be split across subagents?
5. What checkpoint file or artifacts will preserve progress?
6. What is the exact resume point if interrupted?

## Best-fit tasks

Use GPT-5.4-only mode for:
- coding
- docs
- research
- implementation plans
- repetitive refactors
- internal tools
- multi-agent parallel builds

## Risk controls

### External APIs
- batch requests
- avoid rapid polling
- serialize writes when needed
- respect retry windows

### Workspace safety
- write artifacts early
- update project trackers if the task is material
- keep raw notes if the task may resume later

### Delegation
- use subagents for isolated, parallel, or long-running branches
- keep the main thread focused on orchestration and reporting

## Resume note template

```markdown
## GPT-5.4 Resume Point
- Deliverable:
- Completed:
- Saved artifacts:
- External blockers/rate limits:
- Next exact step:
```
