# Performance Tracking Guide

## Overview

Performance tracking provides the quantitative foundation for the Self-Smarter-Everyday skill. Without accurate, consistent metrics, the self-improvement loop is flying blind — it can't tell if changes are helping or hurting. This guide covers what metrics to track, how to set up dashboards, how to analyze trends, how to detect anomalies, and how to generate reports that drive improvement decisions.

---

## Metrics to Track

### Primary Metrics

These are the core metrics that directly indicate agent quality.

**1. Response Accuracy Rate**

- **Definition:** Percentage of responses that were correct, complete, and didn't require user correction.
- **Measurement:** Scored during self-audit (0.0-1.0 per interaction, averaged daily).
- **Target:** > 0.80
- **Alert threshold:** < 0.60 for 3+ consecutive days

**2. Token Usage Per Day**

- **Definition:** Total tokens consumed across all interactions in a 24-hour period.
- **Measurement:** Summed from gateway token tracking.
- **Target:** < $7/day cost equivalent
- **Alert threshold:** > $10/day for 3+ consecutive days

**3. Token Usage Per Response**

- **Definition:** Average tokens consumed per individual response.
- **Measurement:** Total tokens / number of responses per day.
- **Target:** Varies by use case. Track trend, not absolute.
- **Alert threshold:** 50% increase over 7-day baseline

**4. Error Rate**

- **Definition:** Percentage of tool calls or interactions that resulted in errors.
- **Measurement:** Error count / total operations per day.
- **Target:** < 5%
- **Alert threshold:** > 15% for any single day

**5. Task Completion Rate**

- **Definition:** Percentage of user-requested tasks that were completed successfully without requiring rework.
- **Measurement:** Tracked via user feedback signals and audit assessment.
- **Target:** > 0.85
- **Alert threshold:** < 0.70 for 3+ consecutive days

### Secondary Metrics

These metrics provide additional context and help diagnose issues.

**6. Average Response Latency**

- **Definition:** Mean time from user message to agent reply start.
- **Measurement:** Timestamp difference from session logs.
- **Target:** < 10 seconds for simple responses, < 30 seconds for complex tasks.

**7. Sub-Agent Utilization**

- **Definition:** Percentage of tasks delegated to sub-agents vs. handled directly.
- **Measurement:** Count of sub-agent spawns / total tasks.
- **Target:** 20-40% for complex workloads. Too high may indicate the parent is over-delegating simple tasks.

**8. Memory Efficiency**

- **Definition:** Ratio of useful memory accesses to total memory accesses.
- **Measurement:** Memory hits that contributed to a better response / total memory reads.
- **Target:** > 0.60

**9. Skill Invocation Success Rate**

- **Definition:** Percentage of skill invocations that completed without errors.
- **Measurement:** Successful skill executions / total skill invocations.
- **Target:** > 0.90

**10. User Satisfaction Signal**

- **Definition:** Composite score from positive/negative user feedback signals.
- **Measurement:** Count of positive signals minus negative signals, normalized.
- **Target:** Positive ratio > 0.75

### Cost Metrics

**11. Daily Operating Cost**

- **Definition:** Total cost of model API calls, sub-agent spawns, and tool usage per day.
- **Measurement:** Tracked from gateway billing data.
- **Target:** < $7/day
- **Alert threshold:** > $10/day

**12. Cost Per Task**

- **Definition:** Average cost to complete one user-requested task.
- **Measurement:** Daily cost / number of tasks completed.
- **Target:** Track trend.

**13. Sub-Agent Cost Overhead**

- **Definition:** Percentage of total cost consumed by sub-agent operations.
- **Measurement:** Sub-agent token cost / total token cost.
- **Target:** < 40%

---

## Dashboard Setup

### Local File Dashboard

The simplest dashboard is a set of markdown files updated by the nightly routine:

**Daily Dashboard** (`data/audit-logs/YYYY-MM-DD-dashboard.md`):

```markdown
# Daily Performance Dashboard — 2026-08-10

## Summary
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Accuracy | 0.82 | > 0.80 | ✅ |
| Token Usage | $5.40 | < $7.00 | ✅ |
| Error Rate | 3.2% | < 5% | ✅ |
| Task Completion | 0.88 | > 0.85 | ✅ |
| User Satisfaction | 0.79 | > 0.75 | ✅ |

## Composite Score: 0.81 (↑ 0.03 from yesterday)

## Alerts
- None

## Trends (7-day)
- Accuracy: ↑ improving
- Token Usage: → stable
- Error Rate: ↓ worsening (investigate)
```

### JSON Metrics Export

For integration with external dashboard tools, the nightly routine generates a structured JSON file:

```json
{
  "date": "2026-08-10",
  "metrics": {
    "accuracy": 0.82,
    "tokenUsagePerDay": 234500,
    "tokenUsagePerResponse": 4989,
    "errorRate": 0.032,
    "taskCompletionRate": 0.88,
    "avgResponseLatencyMs": 8200,
    "subAgentUtilization": 0.35,
    "memoryEfficiency": 0.67,
    "skillSuccessRate": 0.94,
    "userSatisfaction": 0.79,
    "dailyCostUsd": 5.40,
    "costPerTask": 0.27,
    "subAgentCostOverhead": 0.38
  },
  "alerts": [],
  "compositeScore": 0.81,
  "nightlyReportPath": "data/audit-logs/2026-08-10-nightly-report.md"
}
```

### Trend Visualization

For visual trend analysis, generate a simple ASCII chart in the weekly report:

```
Composite Score Trend (14 days)
0.85 |                          *---*
0.80 |              *---*---*
0.75 |    *---*---*
0.70 |---*
     +---+---+---+---+---+---+---+---+---+---+---+---+---+---
     Jul 28                    Aug 4                    Aug 10
```

---

## Trend Analysis

### Short-Term Trends (7-Day)

Analyzed every night. Look for:

- **Sustained improvement** — 5+ consecutive days of increasing scores.
- **Sustained decline** — 3+ consecutive days of decreasing scores. Action required.
- **Oscillation** — Scores bouncing up and down. May indicate inconsistent prompt mutations.
- **Plateau** — Scores stable for 10+ days. May need a different optimization strategy.

### Medium-Term Trends (30-Day)

Analyzed weekly. Look for:

- **Overall trajectory** — Is the agent getting better over the month?
- **Dimension balance** — Are all dimensions improving, or is progress concentrated in one area?
- **Cost efficiency** — Is the cost-per-task trending downward?
- **Capability expansion** — Is the agent handling more complex tasks than before?

### Long-Term Trends (90-Day)

Analyzed monthly. Look for:

- **Compound improvement** — Total improvement since the system was first activated.
- **Regression events** — Periods where performance dropped and how long recovery took.
- **Seasonal patterns** — Does performance vary by day of week, time of month, or workload type?
- **Skill catalog growth** — How has the skill catalog evolved over the quarter?

### Trend Calculation

Use exponential moving average (EMA) for trend lines:

```
EMA(today) = α × value(today) + (1 - α) × EMA(yesterday)
```

Where α = 0.3 for 7-day EMA, α = 0.1 for 30-day EMA.

---

## Anomaly Detection

### What Constitutes an Anomaly?

An anomaly is a metric value that deviates significantly from its expected range.

**Detection methods:**

**1. Standard Deviation Method**

Calculate the mean and standard deviation of each metric over the past 30 days. Flag any value more than 2 standard deviations from the mean.

```
anomaly = |value - mean| > 2 × stddev
```

**2. Percentage Change Method**

Flag any metric that changes by more than a threshold percentage from the previous day:

| Metric | Alert Threshold |
|--------|-----------------|
| Composite score | > 15% drop |
| Token usage | > 50% increase |
| Error rate | > 100% increase (doubles) |
| Response latency | > 100% increase |
| Cost | > 50% increase |

**3. Absolute Threshold Method**

Flag any metric that crosses a predefined absolute threshold (the alert thresholds listed in the metrics section above).

### Anomaly Response

When an anomaly is detected:

1. **Log the anomaly** in the nightly report with full context.
2. **Attempt root cause analysis** — correlate with other anomalies, recent changes, and known events.
3. **Suggest remediation** — based on the error pattern library and historical recovery actions.
4. **Escalate if critical** — if the anomaly indicates a critical failure, flag for human attention.

---

## Reporting Formats

### Daily Report

Generated every night. Contains:

- Metric summary table with target comparison
- Composite score and trend direction
- Alerts (if any)
- Changes made during nightly routine (prompt mutations, memory compaction, skill changes)
- Top 3 accomplishments of the day
- Top 3 areas for improvement

### Weekly Report

Generated every Sunday night. Contains:

- Week-in-review summary
- 7-day trend charts (ASCII)
- Dimension-by-dimension analysis
- Prompt mutations attempted and their outcomes
- Skills created, modified, or retired
- Memory compaction statistics
- Cost analysis (total weekly cost, average daily cost, cost trend)
- Recommendations for the coming week

### Monthly Report

Generated on the 1st of each month. Contains:

- Month-in-review executive summary
- 30-day trend analysis
- Capability assessment (what can the agent do now that it couldn't a month ago?)
- Prompt evolution summary (total mutations, success rate, net improvement)
- Skill catalog evolution
- Memory health assessment
- Cost analysis with projections
- Strategic recommendations

---

## Historical Comparison

### Comparison Methodology

To compare current performance against historical baselines:

1. **Load baseline metrics** from `data/prompt-versions/baseline.json`
2. **Load current metrics** from today's metrics file
3. **Calculate deltas** for each metric
4. **Determine statistical significance** using the sample sizes and variance

### Comparison Report Format

```markdown
## Performance Comparison: Current vs. Baseline

| Metric | Baseline (Aug 10) | Current (Sep 10) | Change | Significance |
|--------|-------------------|-------------------|--------|--------------|
| Accuracy | 0.76 | 0.84 | +0.08 | Significant (p<0.05) |
| Token Efficiency | 0.68 | 0.77 | +0.09 | Significant (p<0.05) |
| Response Time | 0.81 | 0.82 | +0.01 | Not significant |
| Error Rate | 0.72 | 0.85 | +0.13 | Significant (p<0.01) |
| User Satisfaction | 0.74 | 0.80 | +0.06 | Significant (p<0.05) |
| **Composite** | **0.74** | **0.82** | **+0.08** | **Significant** |

### Key Insights
- Largest improvement: Error Rate (+0.13) — error pattern library is working
- Smallest improvement: Response Time (+0.01) — this is largely model-dependent
- All improvements are statistically significant except Response Time
- At current trajectory, projected composite score in 30 days: 0.86
```

---

## Summary

Performance tracking turns subjective impressions ("the agent seems better") into objective measurements ("composite score improved from 0.74 to 0.82 over 30 days, with statistically significant improvements in 4 of 5 dimensions"). The metrics, dashboards, trend analysis, and anomaly detection systems described in this guide provide the data infrastructure that makes the Self-Smarter-Everyday skill effective. Without tracking, there's no way to know if the nightly routine is actually helping. With tracking, every improvement is quantified, every regression is caught early, and every decision is data-driven.
