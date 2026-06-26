## Description: <br>
Generate QuickBooks Online mileage CSV files from Airtable, Outlook, or Google Calendar records using the local qbo-mileage CLI and user-owned credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oasiseng](https://clawhub.ai/user/oasiseng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate, review, or schedule QuickBooks Online mileage CSV files from calendar or inspection records. It helps produce deterministic CSV exports and run reports from user-owned configuration and credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use mileage, address, calendar or inspection data, distance APIs, and configured email or OAuth credentials. <br>
Mitigation: Install and run it only when that access is acceptable, and keep credentials intentionally configured and protected. <br>
Risk: Email delivery can send mileage reports and CSV attachments to a configured recipient. <br>
Mitigation: Keep email disabled unless delivery is intended, verify the recipient, and use dry-run or skip-email before unattended runs. <br>
Risk: Generated mileage CSV files and deduction totals may affect bookkeeping or tax workflows. <br>
Mitigation: Review run_report.md and warnings before using the CSV for bookkeeping or taxes. <br>


## Reference(s): <br>
- [QuickBooks Mileage CSV on ClawHub](https://clawhub.ai/oasiseng/qbo-mileage) <br>
- [Microsoft Graph sendMail endpoint](https://graph.microsoft.com/v1.0/me/sendMail) <br>
- [Gmail API send message endpoint](https://gmail.googleapis.com/gmail/v1/users/me/messages/send) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [CSV files, Markdown run reports, and concise execution guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are normally written under quickbooks_mileage/YYYY-MM/ and may be emailed when email output is enabled.] <br>

## Skill Version(s): <br>
1.0.1 (source: CHANGELOG, pyproject.toml, plugin.json, package __version__, released 2026-06-10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
