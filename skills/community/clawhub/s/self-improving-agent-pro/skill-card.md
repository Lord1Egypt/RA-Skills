## Description:

Local skill for capturing agent errors, corrections, learnings, and recurring patterns, then returning structured insights and suggested rules for future behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kennyzir](https://clawhub.ai/user/kennyzir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to process local improvement events after failures, corrections, or repeated patterns. It helps them review actionable insights and candidate rules before adding durable behavior to an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated rules from untrusted errors or user corrections may introduce incorrect or misleading behavior if applied automatically.

Mitigation: Show suggested rules to a trusted operator for review before adding them to persistent agent memory or configuration.

Risk: Learning events can contain sensitive operational or user details.

Mitigation: Redact sensitive details before submission and apply clear scope, retention, audit, and rollback controls for any stored learnings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kennyzir/skills/self-improving-agent-pro)
- [Claw0x skill page](https://claw0x.com/skills/self-improving-agent)
- [Claw0x developer docs](https://claw0x.com/docs)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [JSON object with processed entries and an optional batch summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns severity, tags, actionable insights, and suggested rules; it does not persist memory by itself.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
