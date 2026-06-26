# Orchestration Patterns Reference

## Multi-Skill Orchestration Recipes

### Pattern 1: Sequential Pipeline

**When:** Output of Skill A is input for Skill B.

```
User: "Generate an image of today's stock market trend"
→ Skill A: astock-daily-brief (fetch market data → output: structured text)
→ Skill B: text-to-image-free (take market summary → generate visualization)
→ Deliver final image
```

**Handoff template:**
```markdown
[Orchestration] Handoff: astock-daily-brief → text-to-image-free
Context: User wants visual representation of market data
Skill-A result: {summary text of today's A-share market}
Skill-B instruction: "Create an infographic-style image based on this market data summary"
```

### Pattern 2: Parallel Fan-Out

**When:** Multiple independent tasks from one request.

```
User: "Give me today's morning news and generate an image of a cyberpunk city"
→ Skill A: morning-news-daily (fetch news)
→ Skill B: text-to-image-free (generate image)
   (Both independent — can run simultaneously)
→ Merge and deliver as a single response
```

### Pattern 3: Conditional Orchestration

**When:** Task B only runs if Task A meets certain criteria.

```
User: "Check the market. If it's down significantly, generate a worried face image"
→ Skill A: astock-daily-brief (check market)
→ Decision point: is market down >2%?
   ├── Yes → Skill B: text-to-image-free ("worried investor face")
   └── No → Skip B, just deliver market summary
```

### Pattern 4: Recursive Decomposition

**When:** A request requires a multi-level breakdown.

```
User: "Help me analyze this investment thesis"
→ Root: Analyze investment thesis
  ├── 1. Gather data (astock-daily-brief)
  ├── 2. Identify risks (general reasoning)
  ├── 3. Generate report structure (general knowledge)
  └── 4. Create visualization (text-to-image-free)
→ All sub-tasks complete → compose final deliverable
```

## Skill Conflict Resolution

| Conflict | Resolution |
|----------|------------|
| Two skills match same description | Pick the one with higher success_rate in usage log |
| Skill suggests something another skill contradicts | Flag both to user with reasoning |
| No skill matches but request is complex | Decompose into primitives, solve each with general knowledge |
| Skill requires API key that's missing | Gracefully fallback, inform user of capability gap |

## Performance Fallback Chain

When a skill fails, the orchestration layer should attempt fallbacks:

1. First attempt: primary skill
2. First fallback: same task with general knowledge (no skill)
3. Second fallback: simplified version of the request
4. Last resort: inform user with partial results and next steps

## Logging Handoffs

Each orchestrated flow should produce a lightweight execution log:

```json
{
  "execution_id": "exec_20260519_001",
  "timestamp": "2026-05-19T06:00:00+08:00",
  "trigger": "daily morning routine",
  "flow": "sequential",
  "steps": [
    { "skill": "morning-news-daily", "status": "success", "duration_s": 12 },
    { "skill": "text-to-image-free", "status": "success", "duration_s": 45 }
  ],
  "user_facing": true,
  "result_delivered": true
}
```

Maintain last 100 execution logs; older ones are rotated out.
