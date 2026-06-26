---
name: sharpagent-self-evolving
version: 1.0.0
description: "SharpAgent Self-Evolving Loop — An automated 'Think→Do→Learn' cycle. Fuses the Self-Improving Agent's reflection mechanism with the autoresearch experimental validation paradigm. After every task, automatically reflects on improvements, designs experiments to test hypotheses, absorbs lessons, and archives them as learning records. Makes agents smarter with use."
metadata:
  openclaw:
    emoji: "🧬"
    tags:
      - self-improving
      - agent-evolution
      - learning-loop
      - reflection
      - sharpagent
      - workflow
---

# SharpAgent Self-Evolving Loop v1.0.0

> **Make your agent smarter with every task.**
> The end of one task is the starting point for the next evolution.
> Fuses the two key discoveries from R2: Self-Improving Agent reflection × autoresearch experiment verification.

## Core Philosophy

Most agents finish a task and stop. The next time a similar problem comes up, it starts from scratch. No accumulation.

SharpAgent's self-evolving loop breaks this cycle:

```
① Execute task → ② Reflect ("What could be better?")
                   ↓
⑤ Absorb lesson → ③ Form improvement hypothesis
                   ↓
                ④ Run small experiment to verify
                     ↓
            (back to ②)
```

Every task is an evolution. It doesn't get more expensive with use — it gets more accurate.

## Contract

```yaml
contract:
  name: sharpagent-self-evolving
  version: "1.0.0"
  category: workflow
  trust_level: verified
  reads:
    - Task
    - LearningEntry
    - FiveFactorResult
  writes:
    - LearningEntry
    - ImprovementHypothesis
  preconditions:
    - "A completed task exists to reflect on"
    - "Access to read task output and logs"
  postconditions:
    - "Reflection produces at least 1 improvement hypothesis"
    - "If hypothesis is verifiable, an experiment is designed"
    - "Experiment outcome is recorded as LearningEntry"
  calibration:
    default_mode: professional
    modes_supported: [professional, deep]
  compliance:
    jurisdiction: global
    safety_level: standard
  lifecycle:
    status: active
    publish_as: SharpAgent
```

## Lifecycle: 4-Phase Evolution Loop

```
 ┌─────────────────────────────────────────────┐
 │                                              │
 │   [1. REFLECT] → [2. HYPOTHESIZE]           │
 │       ↑                        ↓             │
 │   [4. ABSORB]  ←  [3. EXPERIMENT]           │
 │                                              │
 └─────────────────────────────────────────────┘
```

### Phase 1: REFLECT — Analyze

After every task, do a structured reflection.

**When:**
- Every task completion (mandatory)
- Major errors mid-task (force deep mode)
- Daily summary (optional, merge multiple reflections)

**Reflection Framework:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧬 Task Reflection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Task: {task_name}
⏱  Duration: {duration}

🟢 What went right?
- {2-3 specific, quantifiable things}

🟡 What could improve?
- {1-3 things that could be better}

🔴 Clear mistakes?
- {If any: description + root cause + impact}

💡 Lesson learned
- {One-sentence lesson}

🧪 Improvement hypothesis
- {One clear, verifiable hypothesis}
```

**Five-Factor Review Embedding**: If the task involves information judgments, run each practice and lesson through the five factors:

```
🔗 Was my source credible?
🧠 Was my reasoning chain complete?
🌍 Compliance check?
🏳️ Any bias in chosen direction?
🔄 Any other sources to cross-verify?
```

---

### Phase 2: HYPOTHESIZE — Form Hypothesis

Refine improvement ideas into **verifiable hypotheses**.

**Hypothesis Format:**

```
IF [I change approach] THEN [expected improvement] BECAUSE [reason]
```

**Good vs Bad Hypotheses:**

| Bad | Good |
|-----|------|
| "Write better next time" | "If I plan an outline for 30s before writing, title quality improves 20%" |
| "Check more sources" | "If I check 2 independent sources before deciding, cross-validation score improves 15%" |
| "Don't make that error again" | "If I add contract validation before commit, bug rate drops 30%" |

**Hypothesis Tiers:**

| Tier | Meaning | Action |
|------|---------|--------|
| 🟢 P0 | Critical improvement, fast (<5 min) | Experiment immediately |
| 🟡 P1 | Valuable, moderate effort (<30 min) | Queue for experiment |
| 🔴 P2 | Long-term, significant investment | Record, experiment when possible |

**If reflection yields no improvement hypothesis** → Check whether there's genuinely no room for improvement. 90% of the time the reflection wasn't honest enough.

---

### Phase 3: EXPERIMENT — Verify

This is the core borrowed from autoresearch (karpathy/autoresearch ⭐80K).

**Don't trust intuition that something is "better" — run a small experiment to prove it.**

**Experiment Cycle** (borrowing autoresearch's 5-minute fixed budget):

```yaml
experiment:
  budget: 5 min              # Fixed time budget
  hypothesis: "..."          # Hypothesis to verify
  setup:                     # Experiment setup
    - control: old approach
    - treatment: new approach
  measurements:              # Metrics
    - metric_1: "completion time"
    - metric_2: "error rate"
    - metric_3: "quality score"
  result:                    # Fill after experiment
    - metric_1: old=12s new=8s ✅
    - metric_2: old=3% new=1% ✅
    - metric_3: old=7/10 new=8.5/10 ✅
  verdict:                   # Conclusion
    - hypothesis_supported: true/false
    - adopt: yes/no/partial
    - notes: ""
```

**Experiment Types:**

| Type | Description | Budget |
|------|-------------|--------|
| A/B comparison | Run old vs new, compare results | 5 min |
| Ablation | Remove one step to see impact | 5 min |
| Boundary test | Test stability under edge conditions | 3 min |
| Cross-verification | Different sources/methods for consistency | 5 min |

**Experiment Discipline:**
1. Write hypothesis before experiment (prevents post-hoc rationalization)
2. Control variables — change one thing at a time
3. Record data, not feelings
4. Failed experiments are still learning

---

### Phase 4: ABSORB — Archive

Record the result regardless of success or failure. This is the fuel for evolution.

**Archive as LearningEntry:**

```json
{
  "type": "LearningEntry",
  "category": "evolution",
  "task_ref": "xxx",
  "source": "self-evolving-loop",
  "lesson": "Planning outline first improved title quality 20%",
  "evidence": "A/B experiment: control=7/10, treatment=8.5/10, n=5",
  "adopted": true,
  "applied_count": 0,
  "created_at": "2026-05-11T06:05:00Z",
  "expiry": null
}
```

**Category Tags:**

| Category | Meaning | Action |
|----------|---------|--------|
| `coding-pattern` | Code pattern improvement | Auto-apply on next coding task |
| `info-source` | Information source improvement | Update monitor source priority |
| `workflow` | Workflow optimization | Update engineering lifecycle gates |
| `tool-usage` | Tool usage skill | Efficiency sequence |
| `domain-knowledge` | Domain knowledge accumulation | Long-term memory |

**Auto-Propagation:**
- If `coding-pattern` → write to `~/.agent-templates/`
- If `info-source` → update monitor config
- If `workflow` → check if engineering lifecycle needs update
- If lesson verified ≥3 times → promote to `verified-best-practice`

---

## Full Cycle Example

```
Task: Analyze an AI paper

① Reflection
✅ Good: Structured extraction of method/results/limitations
🟡 Improve: Abstract always too long, user loses patience
🔴 Error: Forgot to check arXiv for updated version
💡: 150-char abstracts are read more often than 300-char ones

② Hypothesis
IF limit abstract to 150 chars THEN user read rate improves 30%
BECAUSE last analysis (300 chars) was only read halfway

③ Experiment
A/B: Same paper, 300-char version vs 150-char version
Result: 150-char version fully read, 300-char interrupted
Conclusion: ✅ Hypothesis supported, adopt

④ Absorb
Record as workflow lesson, update monitor output template
```

## Edge Cases

| Situation | Action |
|-----------|--------|
| Task execution failed | Force deep reflection mode, focus on root cause |
| 3 consecutive experiment failures | Question hypothesis itself, check experiment design |
| Tiny task (rename variable) | Skip loop, but log if recurring error pattern |
| Multiple reflections same day | Merge into daily evolution summary |
| Hypothesis too abstract | Break into verifiable sub-hypotheses |
| User says "no reflection needed" | Skip but log to preference profile |

## Quality Gates

| Check | What | Fail action |
|-------|------|-------------|
| Reflection output | At least 1 improvement hypothesis | Reflect again |
| Hypothesis verifiable | Has clear A/B or ablation plan | Require refinement |
| Experiment has data | Numbers not "feelings" | Retest or mark unverifiable |
| Absorb archived | Experiment result saved as LearningEntry | Force archive |
| Self-reference | Don't repeat same hypothesis weekly | Mark as duplicate |

## Integration Points

### Five-Factor Review
- Phase 1 reflection judgments run through five factors
- Learning entries carry FiveFactorResult as provenance

### Engineering Lifecycle
- Phase 2 hypothesis = engineering **improvement proposal**
- Phase 3 experiment = **verification phase**
- Successful experiments auto-update lifecycle best practices

### Intelligence Monitor
- Source evolution: unreliable sources from reflection auto-downranked in monitor

## Version History

- **v1.0.0** — Initial release. 4-phase self-evolving loop: Reflect → Hypothesize → Experiment → Absorb.

---

*SharpAgent · MIT-0 · 2026-05-11*
