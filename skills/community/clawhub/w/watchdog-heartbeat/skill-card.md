## Description:

Monitor service health, heartbeat freshness, stuck workflows, and trigger recovery or degraded mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunbinnju-star](https://clawhub.ai/user/sunbinnju-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to review service liveness, heartbeat freshness, stuck workflows, and recovery recommendations for a resident OpenClaw system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recovery recommendations could affect service availability if restart or degraded-mode authority is broader than intended.

Mitigation: Keep the monitored service list and any authority to restart or degrade services explicitly scoped by environment controls.

Risk: Incomplete monitoring data can lead to unknown service health or missed failures.

Mitigation: Surface missing monitoring fields as observability gaps, report affected services as unknown, and escalate gaps on critical services.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Structured Markdown or JSON-like operational summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports service health, expired heartbeats, stuck workflows, recovery recommendations, degraded-mode impact, and observability gaps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
