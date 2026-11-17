## Description:

Harden OpenClaw agent deployments with SSH lockdown, firewall rules, automated security audits, secret rotation reminders, RAM/process monitoring, and CVE alerting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nogravedev](https://clawhub.ai/user/nogravedev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide security hardening, audit workflows, exposure checks, monitoring, and incident response for OpenClaw agent deployments on local machines, VPS hosts, and small devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic process killing could disrupt legitimate workloads if used without review.

Mitigation: Require explicit approval before killing processes and scope actions to named hosts or processes.

Risk: Recurring audits and outbound reports can expose sensitive security findings.

Mitigation: Configure report destinations deliberately, limit report contents, and disable scheduled monitoring when it is no longer needed.

Risk: Secret scans and local security inspections may access sensitive files or personal machines.

Mitigation: Run only in environments where local inspection is authorized and review proposed commands before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nogravedev/skills/security-essentials)
- [ClawKits Publisher Site](https://clawkits.xyz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with prioritized findings, checklists, playbooks, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local scans, cron setup, process actions, and outbound reports that require explicit user approval.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
