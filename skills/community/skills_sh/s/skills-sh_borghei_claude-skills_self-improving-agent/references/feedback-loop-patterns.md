# Feedback Loop Patterns

Read this when designing how the agent captures outcomes, classifies feedback, detects performance regressions, and runs the learning/regression workflows. Includes the core improvement-loop architecture, the operational workflows, common pitfalls, troubleshooting, and the success-criteria bar.

## Core Architecture

### The Improvement Loop

```
┌──────────────────────────────────────────────────────────┐
│                   SELF-IMPROVEMENT CYCLE                  │
│                                                          │
│  ┌─────────┐    ┌──────────┐    ┌─────────────┐        │
│  │ Execute  │───▶│ Evaluate │───▶│ Extract     │        │
│  │ Task     │    │ Outcome  │    │ Learnings   │        │
│  └─────────┘    └──────────┘    └─────────────┘        │
│       ▲                               │                  │
│       │                               ▼                  │
│  ┌─────────┐    ┌──────────┐    ┌─────────────┐        │
│  │ Apply   │◀───│ Promote  │◀───│ Validate    │        │
│  │ Rules   │    │ to Rules │    │ Learnings   │        │
│  └─────────┘    └──────────┘    └─────────────┘        │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Improvement Maturity Levels

| Level | Name | Mechanism | Example |
|-------|------|-----------|---------|
| 0 | Stateless | No memory between sessions | Default agent behavior |
| 1 | Recording | Captures observations, no action | Auto-memory logging |
| 2 | Curating | Organizes and deduplicates observations | Memory review + cleanup |
| 3 | Promoting | Graduates patterns to enforced rules | MEMORY.md entries become CLAUDE.md rules |
| 4 | Extracting | Creates reusable skills from proven patterns | Recurring solutions become skill packages |
| 5 | Meta-Learning | Adapts learning strategy itself | Adjusts what to capture based on what proved useful |

Most agents operate at Level 0-1. This skill provides the machinery for Levels 2-5.

## Feedback Loop Design

### Outcome Classification

Every agent task produces an outcome. Classify it:

```
SUCCESS         - Task completed, user accepted result
PARTIAL         - Task completed but required corrections
FAILURE         - Task failed, user had to redo
REJECTION       - User explicitly rejected approach
TIMEOUT         - Task exceeded time/token budget
ERROR           - Technical error (tool failure, API error)
```

### Signal Extraction from Outcomes

| Outcome | Signal | Memory Action |
|---------|--------|---------------|
| SUCCESS (first try) | Approach works well | Reinforce (increment confidence) |
| SUCCESS (after correction) | Initial approach had gap | Log the correction pattern |
| PARTIAL (user edited result) | Output format or content gap | Log what user changed |
| FAILURE | Approach fundamentally wrong | Log anti-pattern with context |
| REJECTION | Misunderstood requirements | Log clarification pattern |
| Repeated ERROR | Tool or environment issue | Log workaround or fix |

### Feedback Capture Template

```markdown
## Learning: [Short description]

**Context:** [What task was being performed]
**What happened:** [Outcome description]
**Root cause:** [Why the outcome occurred]
**Correct approach:** [What should have been done]
**Confidence:** [High/Medium/Low]
**Recurrence:** [First time / Seen N times]
**Action:** [KEEP / PROMOTE / EXTRACT]
```

## Performance Regression Detection

### Metrics to Track

| Metric | Measurement | Regression Signal |
|--------|-------------|-------------------|
| First-attempt success rate | Tasks accepted without correction | Dropping below 70% |
| Correction count per task | User edits after agent output | Rising above 2 per task |
| Tool error rate | Failed tool calls / total calls | Rising above 5% |
| Context relevance | Retrieved context actually used | Dropping below 60% |
| Task completion time | Turns to complete task | Rising trend over 5 sessions |

### Regression Response Protocol

```
1. DETECT: Metric crosses threshold
2. DIAGNOSE: Compare recent sessions vs baseline
   - What changed? (New code? New patterns? New tools?)
   - Which task types are affected?
   - Is it a memory issue or a capability issue?
3. RESPOND:
   - Memory issue → Review and curate MEMORY.md
   - Stale rules → Update CLAUDE.md
   - New code patterns → Add rules for new patterns
   - Capability gap → Extract as skill request
4. VERIFY: Track metric for next 3 sessions
```

## Workflows

### Workflow 2: Post-Session Learning Capture

```
1. Review session outcomes (successes, corrections, failures)
2. For each correction: log what was wrong and what was right
3. For each failure: log root cause and correct approach
4. Check existing memory for related entries
5. If related entry exists: increment recurrence count
6. If new: add entry with context
7. If recurrence threshold met: flag for promotion
```

### Workflow 3: Regression Investigation

```
1. Identify the degraded metric
2. Pull last 5 sessions' outcomes for that task type
3. Compare against baseline (first 5 sessions)
4. Identify what changed: memory, code, rules, environment
5. Propose fix: update rule, add rule, retrain pattern
6. Apply fix
7. Monitor next 3 sessions
```

## Common Pitfalls

| Pitfall | Why It Happens | Fix |
|---------|---------------|-----|
| Memory bloat | Auto-capture without curation | Weekly review, enforce 200-line limit |
| Stale rules | Code changes, rules don't update | Timestamp rules, periodic re-verification |
| Over-promotion | Promoting one-off patterns as rules | Require 3+ recurrences before promotion |
| Silent regression | No metrics tracking | Implement outcome classification |
| Cargo cult rules | Copying rules without understanding | Each rule must have a "why" annotation |
| Contradiction spirals | New rules conflict with old rules | Belief revision protocol |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| MEMORY.md exceeds 200 lines and keeps growing | Auto-capture enabled without scheduled curation | Run the Weekly Memory Health Check workflow; split topic-specific entries into `memory/<topic>.md` files |
| Promoted rules contradict each other | Two conflicting patterns both crossed the 3-recurrence threshold | Apply the Belief Revision protocol -- compare confidence scores, resolve the conflict, delete the weaker rule |
| Agent performance degrades after a promotion batch | Newly promoted rules interact badly or are overly prescriptive | Roll back the most recent promotions, re-validate each rule in isolation, and promote incrementally |
| Skill extraction produces a package that only works on the original project | Generalization step was skipped or rushed | Revisit Extraction Process Step 2 -- strip project-specific details, parameterize hardcoded values, test on a second project before packaging |
| Feedback loop captures noise (trivial observations dominate) | Capture strategy has not been calibrated with the Adaptive Capture Strategy | After 10 sessions, analyze promotion rates by category and restrict capture to high-value categories (error resolutions, user corrections, tool preferences) |
| Regression Detection flags false positives | Thresholds set too aggressively for early-stage projects | Widen thresholds during the first 20 sessions (e.g., first-attempt success 60% instead of 70%), then tighten once a stable baseline exists |
| Confidence scores decay too fast on valid long-term rules | Recency factor penalizes rules that are infrequently encountered but still correct | For rules explicitly confirmed by the user, override the recency factor to 1.0 regardless of age |

## Success Criteria

- **First-attempt success rate above 80%** after 20 sessions of active self-improvement, measured as tasks accepted without user correction.
- **Memory size stays under 200 lines** in MEMORY.md at all times, with overflow correctly routed to topic files.
- **Promotion rate of 15-25%** of captured observations within 30 days, indicating the capture strategy targets high-value signals.
- **Zero stale rules** remaining after each Weekly Memory Health Check -- every rule references current code, tools, and workflows.
- **Regression detection latency under 3 sessions** -- performance degradation is flagged within 3 sessions of onset, not discovered weeks later.
- **Extracted skills reusable across 2+ projects** without modification, validating that the generalization step produces genuinely portable packages.
- **Contradiction resolution within 1 session** -- conflicting rules are detected and resolved via the Belief Revision protocol before they cause downstream errors.
