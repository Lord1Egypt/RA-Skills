## Description:

Proactive self-monitoring of infrastructure, services, and health that tracks disk, memory, load, service health, cron job status, and recent errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suryast](https://clawhub.ai/user/suryast)

### License/Terms of Use:

MIT

## Use Case:

Developers and infrastructure operators use this skill to generate monitoring checks, health reports, and operational guidance for disks, memory, service status, cron jobs, and recent system errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill proposes broad cleanup actions for old system logs, cache files, temporary files, and pip caches.

Mitigation: Keep cleanup in report-only mode unless a user explicitly approves each deletion, and scope any cleanup to reviewed paths.

Risk: Recurring health checks or service restarts can affect host availability if run unattended or with elevated privileges.

Mitigation: Require explicit approval before restarts, avoid running scheduled checks as root, and review the exact script and log destination before scheduling.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and cron code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that inspect local system state and recommended remediation steps.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
