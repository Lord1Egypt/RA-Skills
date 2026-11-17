## Description:

Use when the main operator needs to turn the nightly shortlist into a Telegram morning report with inline approve/reject/later buttons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omermesebuken1](https://clawhub.ai/user/omermesebuken1)

### License/Terms of Use:

MIT-0

## Use Case:

Operators and automation maintainers use this skill to build a short morning report from shortlisted ideas and send it to Telegram with inline approval actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run external local scripts with broad environment access.

Mitigation: Review local script dependencies before installation and pass only the minimum environment variables needed for report building and delivery.

Risk: The skill may send local idea data and delivery metadata beyond the obvious report payload.

Mitigation: Preview Telegram-bound content and document the Notion, Telegram, and delivery-audit fields that are sent before enabling production use.

## Reference(s):

- [Report schema](references/report-schema.md)
- [ClawHub skill page](https://clawhub.ai/omermesebuken1/skills/report-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and JSON report payload guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Telegram-ready report text, inline button callback data, JSON payload files, and blocked-status JSON when required environment configuration is missing.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
