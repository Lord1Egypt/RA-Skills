## Description:

Generate QuickBooks Online mileage CSV files from Airtable, Outlook, or Google Calendar records using the local qbo-mileage CLI and user-owned credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oasiseng](https://clawhub.ai/user/oasiseng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to generate, review, or schedule QuickBooks Online mileage CSV exports from calendar or inspection data. It guides the agent to run the deterministic local CLI, inspect the run report, and surface skipped events, missing addresses, distance failures, and personal-mileage deduction checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mileage source data and generated CSV or report attachments can be sent through the configured SMTP, Microsoft Graph, or Gmail account when email output is enabled.

Mitigation: Keep email disabled for local-only use, verify the configured recipient and mail account before running, and review generated attachments before sharing.

Risk: Incorrect month, home base, vehicle, addresses, distance failures, or personal-trip classification can produce misleading mileage records.

Mitigation: Confirm the requested month, home base, vehicle, skipped events, missing addresses, distance warnings, and PERSONAL legs in run_report.md before using the CSV.

## Reference(s):

- [QuickBooks Mileage CSV Skill Page](https://clawhub.ai/oasiseng/skills/qbo-mileage)
- [Publisher Profile](https://clawhub.ai/user/oasiseng)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; generated artifacts include QuickBooks mileage CSV files and run reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written under the configured output directory, normally quickbooks_mileage/YYYY-MM/.]

## Skill Version(s):

1.0.1 (source: server release metadata, pyproject.toml, plugin.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
