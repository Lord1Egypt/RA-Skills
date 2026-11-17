# Self-Audit Implementation Guide

## Overview

Self-audit is the evaluative core of the Self-Smarter-Everyday skill. During each nightly run, the agent examines its own performance across multiple dimensions, assigns quantitative scores, and uses those scores to drive improvement decisions. Without a robust self-audit system, the other phases (memory compaction, prompt evolution, skill gap analysis) lack the signal they need to prioritize their work.

This guide covers what to audit, how to score, how to interpret results, and how to act on findings.

---

## What to Audit

The self-audit system evaluates five primary dimensions. Each dimension captures a different aspect of agent performance. Together, they provide a holistic view of quality.

### 1. Response Accuracy

Accuracy measures whether the agent's responses were correct, helpful, and aligned with the user's intent.

**Signals to evaluate:**

- **Explicit corrections** — Did the user correct the agent's output? How many times? Corrections are the strongest negative signal.
- **Implicit corrections** — Did the user rephrase their question or ask the same thing differently? This often means the first response missed the mark.
- **Task completion rate** — For task-oriented requests (file edits, deployments, searches), was the task actually completed successfully?
- **Factual correctness** — For knowledge-based responses, were facts verified? Were outdated or hallucinated facts present?
- **Instruction adherence** — Did the agent follow explicit instructions in AGENTS.md, SOUL.md, and user requests?

**Scoring rubric:**

| Score | Meaning |
|-------|---------|
| 0.9-1.0 | No corrections needed, task completed perfectly |
| 0.7-0.89 | Minor corrections or clarifications needed |
| 0.5-0.69 | Significant errors that required user intervention |
| 0.3-0.49 | Major errors, task partially completed |
| 0.0-0.29 | Task failed, completely wrong output, or harmful action |

### 2. Token Efficiency

Token efficiency measures whether the agent used an appropriate amount of tokens for its responses. Both over-use (verbose, repetitive) and under-use (terse, incomplete) are penalized.

**Signals to evaluate:**

- **Tokens per response** — Average and total tokens used across all responses today.
- **Tokens per task** — Tokens consumed to complete each task type. Compare to historical baselines.
- **Redundancy ratio** — Percentage of output that repeats information or restates the obvious.
- **Sub-agent token overhead** — For delegated tasks, how much token budget was consumed by coordination vs. actual work?
- **Context window utilization** — Was the context window used efficiently, or was it bloated with irrelevant history?

**Scoring rubric:**

| Score | Meaning |
|-------|---------|
| 0.9-1.0 | Token usage within 10% of optimal baseline |
| 0.7-0.89 | Token usage within 25% of baseline |
| 0.5-0.69 | Token usage within 50% of baseline |
| 0.3-0.49 | Token usage over 50% above baseline |
| 0.0-0.29 | Extreme token waste or critically terse responses |

### 3. Response Time

Response time measures latency between user input and agent output. While the agent doesn't control model inference speed directly, it can influence response time through context management, sub-agent delegation, and prompt complexity.

**Signals to evaluate:**

- **Average response latency** — Mean time from user message to agent reply.
- **P95 response latency** — 95th percentile latency, capturing worst-case scenarios.
- **Time-to-first-action** — How quickly the agent begins executing after receiving a request.
- **Sub-agent coordination overhead** — Time spent spawning and waiting for sub-agents.

### 4. Error Rate

Error rate measures how frequently the agent encounters errors during execution.

**Signals to evaluate:**

- **Tool execution failures** — How many tool calls returned errors? (exec failures, API timeouts, file not found, etc.)
- **Retry frequency** — How often did the agent need to retry a failed operation?
- **Error severity distribution** — What percentage of errors were warnings vs. critical failures?
- **Recovery success rate** — When errors occurred, did the agent recover gracefully or did the task fail?
- **User-reported errors** — Did the user report anything broken or incorrect?

### 5. User Satisfaction

User satisfaction is the most subjective dimension but also the most important. It captures whether the user had a positive experience.

**Signals to evaluate:**

- **Positive explicit feedback** — "Thanks", "perfect", "great job", emoji reactions.
- **Negative explicit feedback** — "Wrong", "try again", "that's not what I asked", frustration signals.
- **Conversation flow** — Were interactions smooth and efficient, or did they require many back-and-forth exchanges?
- **Repeat requests** — Did the user have to ask the same thing multiple times?
- **Tone analysis** — Was the user's tone positive, neutral, or negative across the day's interactions?

---

## Scoring Methodology

### Weighted Composite Score

Each dimension receives an individual score from 0.0 to 1.0. These are combined into a composite score using configurable weights:

```
Composite = (accuracy × 0.30) + (tokenEfficiency × 0.20) + (responseTime × 0.15) + (errorRate × 0.20) + (userSatisfaction × 0.15)
```

The default weights prioritize accuracy and error rate — the two dimensions most directly impacting user experience. Adjust weights in `config.json` based on your priorities.

### Score Normalization

Raw signals are normalized to the 0.0-1.0 range using linear interpolation between defined thresholds. For example, if the baseline for token efficiency is 5000 tokens per response:

- 4500-5500 tokens → score 0.9-1.0
- 3750-6250 tokens → score 0.7-0.89
- 2500-7500 tokens → score 0.5-0.69
- Below 2500 or above 7500 → score decreases further

### Per-Interaction Scoring vs. Aggregate Scoring

Each individual interaction receives a score. The daily audit score is the weighted average of all interaction scores, with optional outlier handling:

- **Median-based scoring** — Uses the median instead of mean to reduce the impact of extreme outliers.
- **Weighted by importance** — Client-facing interactions may be weighted higher than internal housekeeping tasks.
- **Recency weighting** — More recent interactions may be weighted slightly higher to capture improvement trends within the day.

---

## Audit Checklist Template

Use this checklist during each nightly audit to ensure consistency:

```markdown
## Self-Audit Checklist — YYYY-MM-DD

### Data Gathered
- [ ] Session transcripts loaded (count: ____)
- [ ] Memory file changes reviewed
- [ ] Error logs analyzed
- [ ] Token usage statistics collected
- [ ] User feedback signals cataloged

### Accuracy Audit
- [ ] Counted explicit corrections: ____
- [ ] Counted implicit corrections: ____
- [ ] Verified task completion for task-oriented requests
- [ ] Checked factual claims against sources
- [ ] Verified instruction adherence
- [ ] Accuracy score: ____

### Token Efficiency Audit
- [ ] Calculated average tokens per response: ____
- [ ] Compared to baseline: ____
- [ ] Identified top 3 most token-expensive responses
- [ ] Checked for redundancy patterns
- [ ] Token efficiency score: ____

### Response Time Audit
- [ ] Calculated average response latency
- [ ] Identified P95 latency
- [ ] Flagged any responses exceeding 60 seconds
- [ ] Response time score: ____

### Error Rate Audit
- [ ] Counted tool execution failures: ____
- [ ] Counted retries: ____
- [ ] Categorized errors by severity
- [ ] Assessed recovery success rate
- [ ] Error rate score: ____

### User Satisfaction Audit
- [ ] Cataloged positive feedback signals: ____
- [ ] Cataloged negative feedback signals: ____
- [ ] Assessed conversation flow efficiency
- [ ] User satisfaction score: ____

### Composite Score: ____
### Changes Recommended: ____
```

---

## Interpreting Results

### Score Trends

A single night's score is less informative than the trend over time. Look for:

- **Sustained improvement** — Scores trending upward over 7+ days indicate the self-improvement loop is working.
- **Plateau** — Scores stable for 14+ days suggest the agent has reached its current capability ceiling. Consider expanding the scope of prompt mutations or adding new skills.
- **Decline** — Scores trending downward indicate regression. Check if recent prompt mutations introduced problems. Consider rolling back to a previous prompt version.
- **Sudden drops** — A single-night score drop of 0.15+ warrants immediate investigation. Common causes: unusual user requests, tool outages, or a bad prompt mutation.

### Score Distribution Analysis

Don't just look at the composite score. Examine the distribution across dimensions:

- **High accuracy, low token efficiency** — The agent is correct but verbose. Focus prompt evolution on conciseness.
- **High token efficiency, low accuracy** — The agent is terse but wrong. It may be cutting corners to save tokens. Adjust the fitness function to penalize incorrect short responses.
- **High accuracy, low user satisfaction** — The agent is correct but its communication style may be off. Review SOUL.md for tone issues.
- **Low error rate, low response time score** — The agent avoids errors but is slow. Consider optimizing context management or reducing sub-agent overhead.

### Contextual Factors

Always interpret scores in context:

- **New user onboarding days** may have lower accuracy scores as the agent learns preferences.
- **Complex project days** may have higher token usage but still be productive.
- **System outage days** will have inflated error rates that aren't the agent's fault.

---

## Acting on Findings

### Automatic Actions

The nightly routine takes automatic actions based on audit results:

| Condition | Action |
|-----------|--------|
| Composite score > 0.8 | No changes needed. Continue current trajectory. |
| Composite score 0.6-0.8 | Minor prompt mutations suggested. Focus on weakest dimension. |
| Composite score 0.4-0.6 | Significant changes needed. Multiple prompt mutations + skill gap review. |
| Composite score < 0.4 | Emergency review. Flag for human attention. Consider prompt rollback. |
| Accuracy < 0.5 for 3+ nights | Rollback to last known good prompt version. |
| Token efficiency < 0.5 for 3+ nights | Aggressive prompt compression. Reduce context window usage. |
| Error rate > 0.5 | Investigate tool failures. May indicate external system issues. |

### Human Review Triggers

Some findings require human attention:

- **Composite score below 0.3** — Something is seriously wrong.
- **Repeated rollback** — If prompts are being rolled back more than once per week, the mutation strategy needs redesign.
- **New error patterns** — Errors the agent hasn't seen before may indicate infrastructure changes.
- **Skill gaps requiring external resources** — If the agent identifies a need for capabilities it can't self-create.

### Feedback Loop

Audit findings feed directly into the other nightly phases:

- **Prompt Evolution** uses audit scores as the fitness function. Mutations that improve the weakest dimension are prioritized.
- **Skill Gap Analysis** focuses on dimensions where the agent consistently underperforms.
- **Memory Compaction** prioritizes retention of memories related to errors and corrections.

---

## Integration with External Systems

### Dashboard Integration

The machine-readable metrics file (`data/audit-logs/YYYY-MM-DD-metrics.json`) can be ingested by external dashboards. The JSON structure includes:

```json
{
  "date": "2026-08-10",
  "compositeScore": 0.78,
  "dimensions": {
    "accuracy": 0.82,
    "tokenEfficiency": 0.75,
    "responseTime": 0.80,
    "errorRate": 0.70,
    "userSatisfaction": 0.83
  },
  "interactionsCount": 47,
  "totalTokensUsed": 234500,
  "errorsCount": 12,
  "mutationsApplied": 1,
  "skillsCreated": 0,
  "memoryCompactionRatio": 0.42
}
```

### Historical Comparison

The audit system maintains a rolling history of daily scores. Use this for trend analysis:

```bash
# Calculate 7-day moving average
cat data/audit-logs/*-metrics.json | jq -s '[.[].compositeScore] | add / length'
```

---

## Summary

Self-audit is the compass that guides all other self-improvement phases. Accurate, consistent auditing ensures the agent improves in the right direction. Invest time in calibrating your scoring rubrics and reviewing audit results regularly. The audit system is only as good as the signals it measures — garbage in, garbage out.
