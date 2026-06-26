# Task Retrospective

Structured self-evaluation for AI agents after completing tasks. Analyze what worked, what failed, and extract reusable patterns to improve future performance. Use after completing complex tasks, debugging sessions, or multi-step workflows.

## Usage

```
Run a retrospective on the task I just completed.
```

Or with specific context:
```
Retrospective: [task description]. 
Outcome: [success/partial/failure].
Time spent: [duration].
What surprised me: [unexpected findings].
```

## How It Works

1. **Reconstruct** — review the task timeline (steps taken, tools used, decisions made)
2. **Evaluate** — score each phase on efficiency, accuracy, and approach quality
3. **Extract** — identify reusable patterns, anti-patterns, and decision heuristics
4. **Record** — generate a structured retrospective for future reference

## Evaluation Dimensions

### Efficiency
- Were there unnecessary steps or dead ends?
- Could tool calls have been batched or parallelized?
- Was the research phase too long or too short?

### Accuracy
- Was the final output correct and complete?
- Were there false starts or incorrect assumptions?
- Did the solution match the actual requirements?

### Approach Quality
- Was the problem decomposition effective?
- Were the right tools chosen for each step?
- Would a different strategy have been faster?

### Learning Extracted
- What new patterns can be reused?
- What anti-patterns should be avoided?
- What domain knowledge was gained?

## Output Format

```markdown
## Task Retrospective

### Summary
[1-2 sentences: what was the task, what was the outcome]

### Timeline
| Phase | Duration | Verdict |
|-------|----------|---------|
| Research | Xm | Efficient / Too long / Insufficient |
| Planning | Xm | Good / Skipped / Over-planned |
| Execution | Xm | Clean / Had rework / Multiple attempts |
| Validation | Xm | Thorough / Skipped / Caught issues |

### What Worked
- [Pattern that should be repeated]

### What Didn't Work
- [Anti-pattern to avoid] → [Better alternative]

### Reusable Patterns
- **Pattern name**: [Description of when and how to apply]

### Key Decisions
- [Decision point] → [Choice made] → [Outcome: good/bad/neutral]

### Improvement Actions
- [ ] [Specific action to improve future performance]
```

## Advanced Usage

### Compare Approaches
```
Compare my approach to [task] with the ideal approach. 
What I did: [steps].
What I should have done: [if known].
```

### Pattern Library
Over time, retrospectives build a pattern library:
```
Review my last 5 retrospectives. What recurring patterns emerge?
Which improvement actions have I actually followed through on?
```

### Team Retrospective
```
Run a retrospective on this multi-agent workflow.
Agents involved: [list].
Handoff points: [where work transferred between agents].
Bottlenecks: [where things slowed down].
```
