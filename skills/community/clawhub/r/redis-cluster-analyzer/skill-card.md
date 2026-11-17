## Description:

Analyze Redis Sentinel and Cluster configurations for high availability, performance, and memory efficiency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, infrastructure engineers, and operations teams use this skill to review Redis Sentinel, Cluster, and standalone deployments for availability, memory, persistence, replication, security, and performance risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Redis configuration files and application connection code may include secrets or production-impacting settings.

Mitigation: Point the skill only at relevant Redis configs and client code, and redact sensitive values where possible.

Risk: Generated remediation may change Redis availability, persistence, security, or performance behavior if applied without review.

Mitigation: Review proposed configuration changes with an operator before applying them to production.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, analysis, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with text topology diagrams, issue rankings, Redis configuration directives, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes health and category scores, critical issues, remediation recommendations, and a priority matrix.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
