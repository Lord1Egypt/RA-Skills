## Description:

Security Constitution provides OpenClaw with a four-level risk control workflow for classifying requests, requiring confirmation for sensitive actions, logging operations, and blocking security-bypass attempts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byronbanck-ai](https://clawhub.ai/user/byronbanck-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to add request-level risk review, owner confirmation, audit logging, and bypass blocking guidance to an OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat-based approval passwords can be exposed in transcripts or reused.

Mitigation: Use an external approval mechanism instead of reusable passwords sent through chat.

Risk: The skill attempts to govern every agent request and depends on policy, identity, hooks, notifications, logs, and approval flow being protected outside the model.

Mitigation: Deploy only in controlled environments where those controls are externally protected, reviewed, and audited before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/byronbanck-ai/skills/security-constitution)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with JSON configuration examples and response templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes risk-level policies, approval flow descriptions, audit-log format, and hook behavior guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
