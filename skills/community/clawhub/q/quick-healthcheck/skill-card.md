## Description:

Quick system health snapshot: OpenClaw version, git status, disk usage, and recent memory activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147258xuan](https://clawhub.ai/user/147258xuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace users can request a quick status check before starting work or diagnosing workspace state. The skill reports the OpenClaw version, recent memory activity, Git status, workspace size, and TODO/FIXME count.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial and flagged an unclear activation phrase; broad activation could run workspace checks unexpectedly.

Mitigation: Review the referenced script before installing and limit activation to explicit health-check requests.

## Reference(s):

- [quick-healthcheck on ClawHub](https://clawhub.ai/147258xuan/skills/quick-healthcheck)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [JSON status snapshot]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One-shot workspace status report.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
