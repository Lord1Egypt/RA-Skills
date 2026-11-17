## Description:

Use when investigating or improving performance, latency, throughput, memory use, CPU use, startup time, or bundle size. Establishes a repeatable baseline and profiles the measured bottleneck before any optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[escoffier-labs](https://clawhub.ai/user/escoffier-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn a performance concern into a repeatable workload, establish and profile a baseline, test a focused optimization, and report comparable results without sacrificing correctness or security.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Benchmarking or profiling against production systems can add load, and retained profiling results may contain sensitive information.

Mitigation: Use a scoped test workload, review commands before running them against production, and handle retained profiling results according to the project's data practices.

Risk: Performance changes may regress correctness, security, durability, or accessibility.

Mitigation: Keep those requirements intact unless the user explicitly approves a tradeoff, and run the relevant correctness and security checks before accepting a change.

## Reference(s):

- [Thermometer on ClawHub](https://clawhub.ai/escoffier-labs/skills/skillet-thermometer)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Workload-specific performance-testing guidance and a Markdown report with commands, measurements, and comparisons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected workload, environment, tools, and measurements; the skill does not guarantee a performance gain.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
