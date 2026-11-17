# Prompt Optimization Guide

## Overview

Prompt optimization is the process by which the Self-Smarter-Everyday skill incrementally improves the agent's system prompts — the instructions that define its behavior, personality, decision-making framework, and operational procedures. Small, well-targeted changes to prompts can produce significant improvements in response quality, token efficiency, and task accuracy. This guide covers the complete prompt optimization lifecycle: baseline measurement, mutation strategies, fitness evaluation, A/B testing, version control, rollback procedures, and measuring improvement.

---

## Baseline Measurement

### Why Baselines Matter

You can't improve what you can't measure. Before any prompt mutation is attempted, the system must establish a performance baseline — a set of metrics that represent the agent's current capability level. This baseline serves as the reference point against which all future mutations are evaluated.

### Establishing the Baseline

The baseline is established during the first nightly run and updated weekly.

**Step 1: Collect Representative Interactions**

Gather 20-50 historical interactions that represent the agent's typical workload. These should cover:

- Simple factual questions (5-10 examples)
- Multi-step task execution (5-10 examples)
- Creative or open-ended requests (5-10 examples)
- Error recovery scenarios (3-5 examples)
- Conversational exchanges (3-5 examples)
- Edge cases and unusual requests (2-5 examples)

**Step 2: Score Each Interaction**

Each interaction is scored across the five audit dimensions (accuracy, token efficiency, response time, error rate, user satisfaction) using the current prompts.

**Step 3: Compute Baseline Metrics**

```
Baseline Accuracy = mean(accuracy scores across all sample interactions)
Baseline TokenEfficiency = mean(token efficiency scores)
Baseline ResponseTime = mean(response time scores)
Baseline ErrorRate = mean(error rate scores)
Baseline UserSatisfaction = mean(user satisfaction scores)
Baseline Composite = weighted average of above
```

**Step 4: Store the Baseline**

The baseline is stored in `data/prompt-versions/baseline.json`:

```json
{
  "established": "2026-08-10",
  "lastUpdated": "2026-08-17",
  "sampleSize": 35,
  "scores": {
    "accuracy": 0.76,
    "tokenEfficiency": 0.68,
    "responseTime": 0.81,
    "errorRate": 0.72,
    "userSatisfaction": 0.74,
    "composite": 0.74
  }
}
```

### Baseline Refresh

The baseline is refreshed weekly (every Sunday night) using the most recent 50 interactions. This prevents the baseline from becoming stale as the agent's capabilities evolve. When the baseline is refreshed, the old baseline is archived for historical comparison.

---

## Mutation Strategies

### What Is a Prompt Mutation?

A mutation is a small, targeted change to one or more system prompts. Mutations are deliberately conservative — each mutation changes only one aspect of the prompt to isolate its effect. Large, sweeping changes are avoided because they make it impossible to attribute improvements or regressions to specific changes.

### Mutation Types

**1. Clarification Mutations**

Add or modify instructions to make ambiguous behavior more precise.

Example:
- Before: "Be concise in responses."
- After: "Be concise in responses. Target under 200 words for simple questions, under 500 for complex explanations. Use bullet points only for lists of 3+ items."

**2. Constraint Mutations**

Add new constraints or modify existing ones to prevent known failure modes.

Example:
- Before: "Don't send messages without permission."
- After: "Don't send messages, emails, or social media posts without explicit permission from the user. Draft content is allowed. When in doubt, show the draft first."

**3. Priority Mutations**

Adjust the ordering or emphasis of instructions to change behavior weighting.

Example:
- Before: Instructions listed in arbitrary order.
- After: Most critical instructions moved to the top with explicit priority markers.

**4. Example Mutations**

Add or modify few-shot examples to guide behavior.

Example:
- Adding a concrete example of the desired response format for a common request type.

**5. Removal Mutations**

Remove instructions that are causing unintended side effects or are redundant.

Example:
- Removing a rule that was added to fix a one-time issue but now causes problems in the general case.

**6. Structural Mutations**

Reorganize the prompt structure for better model comprehension without changing the semantic content.

Example:
- Converting a long paragraph into a numbered list.
- Moving related instructions into a grouped section.

### Mutation Selection

Each night, the system selects which mutations to attempt based on:

1. **Weakest dimension** — Mutations targeting the lowest-scoring audit dimension are prioritized.
2. **Error patterns** — Specific errors from the day inform constraint mutations.
3. **User feedback** — Explicit user requests for behavior changes become mutations.
4. **Historical success** — Mutation types that have worked well in the past are tried first.

### Mutation Limits

To prevent destabilization:

- **Maximum 3 mutations per night** (configurable via `promptEvolution.maxMutationsPerNight`)
- **Each mutation changes only one semantic unit** — one rule, one example, one constraint
- **No mutations to core identity** — SOUL.md persona changes require explicit human approval

---

## Fitness Evaluation

### The Fitness Function

Each mutation is evaluated using a fitness function that measures whether the mutation improved or degraded performance.

**Evaluation process:**

1. **Select test samples** — Draw `fitnessSampleSize` (default: 20) interactions from the historical sample set.
2. **Apply mutation** — Create a temporary prompt variant with the mutation applied.
3. **Re-evaluate** — Score the test samples using the mutated prompt. Since we can't re-run the model with different prompts on historical data, the evaluation uses a proxy: the agent analyzes each historical interaction and predicts how the mutated prompt would have changed the response.
4. **Compare scores** — Compare the predicted scores with the baseline scores.
5. **Decide** — If the composite score improves by at least `minImprovementThreshold` (default: 0.02), the mutation is accepted.

### Proxy Evaluation Method

Since we can't literally re-run historical interactions with different prompts, the fitness evaluation uses a structured analysis approach:

1. The agent reads each historical interaction (user input + actual response).
2. The agent reads both the original prompt and the mutated prompt.
3. The agent predicts: "Given this mutated prompt, how would my response have differed?"
4. The agent scores the predicted response against the same rubric used for actual audit.
5. The comparison between actual scores and predicted scores estimates the mutation's effect.

This is an approximation, not a perfect measurement. The system compensates for this by:

- Using a large enough sample size (20+ interactions)
- Requiring a minimum improvement threshold (0.02) to accept mutations
- Rolling back mutations that cause regression in subsequent nights

### Fitness Scoring Output

```json
{
  "mutation": "Added word count targets to conciseness rule",
  "type": "clarification",
  "testSampleSize": 20,
  "baselineComposite": 0.74,
  "predictedComposite": 0.78,
  "improvement": 0.04,
  "dimensionChanges": {
    "accuracy": 0.00,
    "tokenEfficiency": 0.12,
    "responseTime": 0.02,
    "errorRate": 0.00,
    "userSatisfaction": 0.03
  },
  "decision": "accepted"
}
```

---

## A/B Testing Methodology

### When to Use A/B Testing

For high-impact mutations (changes to core behavioral rules, significant structural changes), the system uses a more rigorous A/B testing approach instead of the proxy evaluation.

### A/B Test Process

**Day 1-3: Baseline Period (A)**

The agent operates with the current prompt (version A). All interactions are logged with full metrics.

**Day 4-6: Test Period (B)**

The agent operates with the mutated prompt (version B). All interactions are logged with the same metrics.

**Day 7: Analysis**

Compare metrics from Period A vs. Period B using statistical tests:

- **T-test** for continuous metrics (token count, response time)
- **Chi-squared test** for categorical metrics (error/no-error, satisfied/not-satisfied)
- **Effect size** calculation to determine practical significance

### Statistical Significance

A mutation is only accepted if:

- p-value < 0.05 (statistically significant)
- Effect size > minimum threshold (practically significant)
- No dimension shows significant regression

### A/B Test Limitations

A/B testing takes 7 days per mutation, which limits throughput to approximately one major mutation per week. This is intentional — major changes deserve careful evaluation. Minor mutations use the faster proxy evaluation.

---

## Version Control for Prompts

### Git-Based Versioning

All prompt versions are tracked in a local git repository at `data/prompt-versions/`:

```bash
cd data/prompt-versions/
git log --oneline
# abc1234 Added word count targets to conciseness rule (fitness: +0.04)
# def5678 Updated error recovery instructions (fitness: +0.02)
# ghi9012 Initial baseline established
```

### Commit Message Format

Each commit includes structured metadata:

```
Added word count targets to conciseness rule

Mutation type: clarification
Target dimension: tokenEfficiency
Fitness improvement: +0.04 (0.74 → 0.78)
Test sample size: 20
Nightly report: data/audit-logs/2026-08-10-nightly-report.md
```

### Branch Strategy

- **main** — the current active prompt version
- **experiment/{name}** — branches for A/B tests in progress
- **rollback/{date}** — branches created during rollback events

---

## Rollback Procedures

### When to Rollback

A rollback is triggered when:

1. **Post-mutation regression** — The composite audit score drops by 0.05+ in the night after a mutation was applied.
2. **Specific dimension collapse** — Any single dimension drops by 0.10+ after a mutation.
3. **User complaints** — Explicit negative feedback that correlates with a recent mutation.
4. **Error spike** — Error rate increases significantly after a mutation.

### Rollback Process

```bash
# 1. Identify the last known good version
cd data/prompt-versions/
git log --oneline -10

# 2. Revert to the previous version
git revert HEAD --no-edit

# 3. Log the rollback
echo "ROLLBACK $(date +%Y-%m-%d): Reverted mutation '$(git log -1 --pretty=%s HEAD@{1}}' due to regression" >> data/audit-logs/rollback-log.md

# 4. Update the nightly report
# The nightly report includes the rollback event and its reason
```

### Rollback Analysis

After a rollback, the system records:

- Which mutation was reverted
- Why it was reverted (which metric regressed)
- What was learned (the mutation hypothesis was wrong because...)
- What to try differently next time

This analysis prevents the same failed mutation from being retried without modification.

---

## Common Optimization Patterns

### Pattern 1: Verbosity Reduction

**Symptom:** Token efficiency score is low. Responses are longer than necessary.

**Mutation:** Add explicit length targets and examples of concise responses.

**Expected improvement:** 0.05-0.15 in token efficiency.

### Pattern 2: Instruction Adherence

**Symptom:** Accuracy score is low. The agent ignores specific rules.

**Mutation:** Move ignored rules higher in the prompt, add emphasis markers, include examples of correct adherence.

**Expected improvement:** 0.03-0.10 in accuracy.

### Pattern 3: Error Recovery

**Symptom:** Error rate is high. The agent gives up too easily on failures.

**Mutation:** Add explicit retry instructions, alternative approaches for common failure modes, and encouragement to try different strategies.

**Expected improvement:** 0.05-0.12 in error rate.

### Pattern 4: Tone Calibration

**Symptom:** User satisfaction is low. Users find the agent's tone too robotic or too casual.

**Mutation:** Adjust SOUL.md tone instructions with specific examples of desired communication style.

**Expected improvement:** 0.03-0.08 in user satisfaction.

### Pattern 5: Tool Selection

**Symptom:** The agent uses the wrong tool for the job, leading to errors or inefficiency.

**Mutation:** Add decision tree or tool selection guide to the prompt with clear criteria for each tool.

**Expected improvement:** 0.05-0.10 in error rate and response time.

---

## Measuring Improvement

### Short-Term Metrics (Nightly)

- Composite score trend (7-day moving average)
- Number of mutations accepted vs. rejected
- Rollback frequency
- Per-dimension score changes

### Medium-Term Metrics (Weekly)

- Week-over-week composite score improvement
- Token usage trend (total tokens per day)
- Error rate trend
- Skill catalog growth

### Long-Term Metrics (Monthly)

- Month-over-month capability expansion (new task types handled successfully)
- Cumulative prompt improvement (comparison to initial baseline)
- Memory efficiency (memory-to-noise ratio)
- User satisfaction trend

### Improvement Reporting

The nightly report includes an improvement section:

```markdown
## 📈 Improvement Tracking

### Current vs. Baseline
| Dimension | Baseline | Current | Change |
|-----------|----------|---------|--------|
| Accuracy | 0.76 | 0.82 | +0.06 |
| Token Efficiency | 0.68 | 0.75 | +0.07 |
| Response Time | 0.81 | 0.83 | +0.02 |
| Error Rate | 0.72 | 0.79 | +0.07 |
| User Satisfaction | 0.74 | 0.78 | +0.04 |
| **Composite** | **0.74** | **0.80** | **+0.06** |

### This Week
- Mutations attempted: 5
- Mutations accepted: 3
- Mutations rolled back: 1
- Net improvement: +0.03
```

---

## Summary

Prompt optimization is a scientific process applied to agent behavior. By establishing baselines, making targeted mutations, evaluating fitness rigorously, and maintaining version control with rollback capability, the system continuously improves the agent's core instructions. The key principles are: small changes, rigorous evaluation, automatic rollback on regression, and patient accumulation of improvements over time. No single mutation transforms the agent — but hundreds of small improvements compound into dramatically better performance over weeks and months.
