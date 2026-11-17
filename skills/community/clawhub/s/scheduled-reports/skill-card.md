## Description:

Define, preview, approve, and manage recurring reports for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xvespertine](https://clawhub.ai/user/0xvespertine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Scheduled Reports to convert recurring reporting requests into approved report definitions and OpenClaw cron jobs. The skill helps define schedules, delivery targets, data sources, previews, approvals, integrity checks, and lifecycle actions for recurring reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring reports can expose or write content through overly broad local paths or delivery targets.

Mitigation: Run OpenClaw cron jobs with least privilege, keep report definitions and previews in private approved directories, restrict folder delivery to an export root, and use administrator-approved webhook aliases.

Risk: A recurring report could be enabled or changed before a reviewer has approved the actual preview artifact and delivery framing.

Mitigation: Require a generated preview artifact, inline approval, validation, integrity hashes, and an activation check in the same cron mode before enabling or changing a report.

Risk: Report data may contain content that tries to influence runtime behavior or delivery choices.

Mitigation: Treat report data as untrusted and prevent data-driven tool calls, recipient changes, query changes, and delivery target changes.

## Reference(s):

- [Scheduled Reports on ClawHub](https://clawhub.ai/0xvespertine/skills/scheduled-reports)
- [Report Definition](references/REPORT_DEFINITION.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON report definitions and validation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces approved recurring-report specifications, cron setup guidance, preview and delivery contracts, and lifecycle instructions.]

## Skill Version(s):

1.4.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
