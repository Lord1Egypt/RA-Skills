## Description:

Optimize retry patterns for flaky or slow agents/services. Use when you see fixed-interval retries, repeated 30s/60s wait loops, Retrying... messages, wrapper timeouts, or performance bottlenecks caused by retry storms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147258xuan](https://clawhub.ai/user/147258xuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to analyze retry configurations, generate settings with bounded exponential backoff and jitter, validate retry limits and error classes, and compare retry wait times in a benchmark simulation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The benign security verdict is not a guarantee of safety, and scanner coverage was incomplete.

Mitigation: Review the bundled skill files before installing, as advised by the security guidance.

## Reference(s):

- [Retry Optimizer on ClawHub](https://clawhub.ai/147258xuan/skills/retry-optimizer)

## Skill Output:

**Output Type(s):** [Configuration, Analysis]

**Output Format:** [JSON configuration and analysis results, plus plain-text benchmark comparisons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configuration analysis, generated retry settings, validation results, and simulated wait-time comparisons.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
