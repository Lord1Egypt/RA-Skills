## Description:

Provides security auditing for Clawdbot deployments, including checks for exposed credentials, open ports, weak configurations, file permissions, Docker risks, and optional auto-fix remediation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianjin-ren](https://clawhub.ai/user/tianjin-ren)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit Clawdbot deployments before release or on a schedule, generate findings, and optionally run remediation for common issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto-fix mode can broadly change deployment file permissions and may disrupt services that require group-readable JSON, key, or certificate files.

Mitigation: Review the planned changes first, keep backups, use least privilege, and avoid --fix unless you have confirmed the affected files under /root/clawd.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianjin-ren/skills/security-audit-tianjin)
- [Publisher profile](https://clawhub.ai/user/tianjin-ren)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON audit report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run read-only audit modes or, with --fix, change file permissions and security-related configuration.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
