## Description:

Performs comprehensive security auditing for OpenClaw deployments, covering environment isolation, privilege checks, port exposure, skill trust sources, process and network state, credential leak checks, integrity baselines, and opt-in backup and notification flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iaadoa](https://clawhub.ai/user/iaadoa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit OpenClaw deployments on laptops, workstations, Raspberry Pi devices, and servers for misconfiguration, exposure, credential leakage, integrity drift, and hardening gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill should be reviewed before installation on sensitive machines because it performs broad local security auditing and writes reports that may contain sensitive operational findings.

Mitigation: Run it as a normal user where possible, review it before installation, and treat generated reports as sensitive material.

Risk: Optional Git backup can push broad local OpenClaw state to a configured remote repository.

Mitigation: Leave SECURITY_AUDIT_ENABLE_GIT unset unless the remote, payload, and repository contents have been reviewed.

Risk: Optional Telegram notifications introduce network communication with an external messaging service.

Mitigation: Leave SECURITY_AUDIT_ENABLE_TELEGRAM unset unless the notification payload, bot token, and chat destination have been reviewed.

Risk: The current documentation may understate write and network behavior around optional backup and notification flows.

Mitigation: Use evidence.security guidance as the review baseline and confirm optional feature boundaries before deployment.

## Reference(s):

- [Security Declaration](SECURITY.md)
- [OpenClaw Security Audit on ClawHub](https://clawhub.ai/iaadoa/skills/security-audit-openclaw)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text security brief and detailed report, with Markdown usage and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Detailed reports are written under /tmp/openclaw-security-reports; optional Git backup and Telegram notification flows require explicit environment variables.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
