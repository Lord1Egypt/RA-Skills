## Description:

Audits authorized remote servers over SSH and helps produce structured security and environment reports covering system state, services, ports, web/database configuration, SSH settings, firewall status, SELinux status, failed logins, cron jobs, and high-memory processes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aowind](https://clawhub.ai/user/aowind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system administrators use this skill to inspect servers they own or are authorized to audit, identify exposed services and insecure SSH or firewall settings, and draft Markdown audit reports with recommended fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit command defaults to the root user for SSH access.

Mitigation: Run it only against authorized hosts and specify a least-privileged audit user whenever possible.

Risk: Generated reports and command output can contain sensitive infrastructure details such as services, ports, SSH settings, web roots, cron jobs, and failed login records.

Mitigation: Store reports locally, restrict access, redact sensitive details before sharing, and avoid committing reports to repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aowind/skills/sjht-server-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with shell command snippets and structured audit findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive infrastructure details collected from authorized SSH targets.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact changelog lists 0.1.0 released 2026-03-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
