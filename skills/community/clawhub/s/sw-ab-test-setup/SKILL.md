# A/B Test Setup Skill

## Trigger
Plan A/B tests with proper methodology — hypothesis, sample size, duration, variant design, statistical significance.

**Trigger phrases:** "A/B test", "split test", "experiment", "test this change", "variant", "multivariate test", "hypothesis"

## Process

1. **Hypothesis**: What are you testing and why?
2. **Metrics**: Primary metric, guardrail metrics, success criteria
3. **Design**: Control vs variant(s), what exactly changes
4. **Calculate**: Sample size, test duration, minimum detectable effect
5. **Plan**: Implementation, QA, analysis timeline

## Output Format

```markdown
# A/B Test Plan: [Name]

## Hypothesis
If we [change], then [metric] will [improve/increase] because [reason].

## Variants
- **Control (A):** [current experience]
- **Variant (B):** [proposed change — be specific]

## Metrics
- **Primary:** [metric] — current: [X%] — target: [Y%]
- **Guardrail:** [metric that should NOT decrease]

## Sample Size & Duration
- MDE: [minimum detectable effect, e.g., 10% relative]
- Sample needed: [N per variant]
- Current traffic: [X visitors/day to test area]
- Estimated duration: [Y days/weeks]
- Confidence level: 95%

## Implementation Notes
[What needs to change, where, any technical considerations]

## Decision Framework
- If primary metric improves ≥ MDE with p < 0.05 → ship variant
- If no significant difference after [duration] → keep control
- If guardrail metric drops > [threshold] → stop test immediately
```

## Rules

- Never run a test without a hypothesis
- One change per test (unless multivariate with sufficient traffic)
- Run for minimum 2 full business cycles (usually 2 weeks)
- Don't peek at results daily — pre-commit to evaluation date
- 95% confidence minimum. 80% power minimum.
- Document everything: future you needs to know why this was tested
