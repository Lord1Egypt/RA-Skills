## Description:

Host security hardening and risk-tolerance configuration for OpenClaw deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1yihui](https://clawhub.ai/user/1yihui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and OpenClaw users use this skill to audit host security posture, plan firewall, SSH, update, backup, and OpenClaw security checks, and apply hardening steps with explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Host hardening changes can disrupt remote access or expected services if applied incorrectly.

Mitigation: Require explicit approval for state-changing actions, confirm how the user connects, stage reversible changes, and include rollback steps before execution.

Risk: Security checks and logs can expose sensitive host details or credential locations.

Mitigation: Ask before running checks, avoid reading credential contents, redact secrets, and store outputs only in user-approved locations.

Risk: Periodic audits or update checks can add persistent scheduled jobs and recurring logs.

Mitigation: Create or modify scheduled checks only after direct approval, use stable job names, and document cadence and output location.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/1yihui/skills/yihui-healthcheck)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and numbered choices]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include remediation plans, rollback notes, audit summaries, and user-approved scheduling guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
