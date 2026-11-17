## Description:

OpenClaw usage and performance reporting that analyzes local session logs to summarize task duration, tool and skill use, model activity, and token consumption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dtsola](https://clawhub.ai/user/dtsola)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and operators use this skill to review local session activity and understand token consumption, task duration, model and tool usage, and skill activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flagged environment-variable access not covered by declared permissions.

Mitigation: Review whether reading OPENCLAW_STATE is appropriate for your deployment and confirm the host runtime's permission limits.

Risk: The security review was partial: three local SKILL.md references were unresolved, and the QR image was outside static-analysis scope.

Mitigation: Review the unresolved local references and inspect the QR image separately before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dtsola/skills/xiaoyaoclaw-usage-report)
- [Project usage documentation (linked in the skill)](https://github.com/dtsola/xiaoyaoclaw-usage-report)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Human-readable text report or JSON summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Aggregated statistics by default; session-level details and full local paths require explicit opt-in flags.]

## Skill Version(s):

1.0.12 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
