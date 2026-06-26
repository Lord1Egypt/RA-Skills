# Scoring Reference

## Three-Layer Scoring

**Layer 1 -- Rule-based** (hard requirements):
- Produced output? Called required tools? Included required fields? Passed schema validation?

**Layer 2 -- Result-based** (objective correctness):
- Answer accuracy vs reference, information completeness, test pass rate

**Layer 3 -- LLM Judge** (soft quality, optional):
- Reasoning depth, professional quality, task completion, A vs B preference

## Six Dimensions (100-point scale)

| Dimension | Weight | Measures |
|-----------|--------|----------|
| Effectiveness | 30 | Task completion, correctness, key objective hits |
| Quality | 20 | Professionalism, clarity, reasoning depth |
| Efficiency | 15 | Token cost, duration, tool call overhead |
| Stability | 15 | Run-to-run variance, edge case resilience |
| Trigger Fitness | 10 | Trigger accuracy, restraint, utility |
| Safety | 10 | Hallucination, verbosity, misleading content |

## Derived Metrics

**Net Gain** = score(with_skill) - score(baseline)

**Value Index** = Net Gain / extra_cost (additional tokens + time)

## Recommendation Thresholds

| Label | Condition |
|-------|-----------|
| Recommended | Net Gain >= 8, no significant regressions |
| Conditionally Recommended | Net Gain >= 3, some category-specific regressions |
| Not Recommended | Net Gain < 0 or significant side effects |
| Needs Revision | Potential exists but current version has clear issues |
| Inconclusive | Real dual-arm execution attempted but evidence insufficient |

## Attribution Dimensions

When scores differ, attribute the cause:

- **Trigger**: Was the skill actually activated?
- **Step**: Did it change the reasoning approach?
- **Tool**: Did it guide better tool usage?
- **Format**: Did it only change formatting, not substance?
- **Side-effect**: Did it add unnecessary complexity?

## Output Format

```markdown
# Skill Evaluation Report: [skill-name]

## Summary
- Recommendation: [LABEL]
- Net Gain: [+/-X.X points]
- Value Index: [X.XX]

## Score Comparison
| Dimension | Baseline | With Skill | Delta |
|-----------|----------|------------|-------|

## Attribution
[Why scores differ]

## Improvement Suggestions
[Actionable changes for the skill author]
```
