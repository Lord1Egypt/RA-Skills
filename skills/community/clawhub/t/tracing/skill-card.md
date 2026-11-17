## Description:

Deep distributed tracing workflow for instrumentation boundaries, context propagation, sampling, tail-based analysis, service maps, and latency debugging when adopting OpenTelemetry, debugging microservices, or tuning P99 latency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeclaw007](https://clawhub.ai/user/mikeclaw007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and site reliability engineers use this skill to plan or improve distributed tracing for microservices, service maps, context propagation, sampling, and latency investigations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tracing plans can expose sensitive span attributes or route telemetry to inappropriate exporter destinations if applied without review.

Mitigation: Review span attributes, retention, and exporter destinations for privacy and cost controls before applying tracing guidance in production.

Risk: High-cardinality attributes or overly broad sampling can increase telemetry storage cost.

Mitigation: Set attribute and span limits, define sampling policy up front, and preserve error visibility while reducing noisy labels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikeclaw007/skills/tracing)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with staged checklists and operational recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable behavior.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
