## Description:

Automate Toingg operations by creating campaigns, scheduling optional analytics pulls, converting Excel contacts, uploading contact lists, and sending WhatsApp template messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhinavpgagi](https://clawhub.ai/user/abhinavpgagi)

### License/Terms of Use:


## Use Case:

Developers and operations users use this skill to automate Toingg campaign creation, analytics collection, contact ingestion, and WhatsApp template outreach from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Campaign payload defaults can enable outbound outreach, autopilot, notifications, and handoff behavior before an operator has reviewed the target workflow.

Mitigation: Review and edit the campaign template before use, especially leadNotificationPhone, leadNotification, outbound/autopilot, and handoff settings.

Risk: Bulk contact uploads and WhatsApp template sends can reach people without valid consent.

Mitigation: Only upload or message contacts when the operator has confirmed proper consent and an approved contact source.

Risk: Generated contact exports and analytics snapshots can contain sensitive operational or personal data.

Mitigation: Store generated files in access-controlled locations and avoid committing contact exports or analytics snapshots to version control.

Risk: Unpinned Python dependencies can change behavior across installations.

Mitigation: Install dependencies in a virtual environment and pin package versions before operational use.

## Reference(s):

- [Analytics Cron Playbook](references/analytics-cron.md)
- [Contact Upload + WhatsApp Template Workflow](references/contact-workflow.md)
- [Toingg Campaign Payload Template](references/payload-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, Python script usage, and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Toingg API JSON responses, analytics snapshots, contact JSON exports, and cron configuration guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
