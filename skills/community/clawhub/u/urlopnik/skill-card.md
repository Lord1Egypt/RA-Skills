## Description:

Urlopnik helps employees in Poland calculate leave days, generate leave-request text or PDF files, and identify favorable leave dates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomasz-pedzierski-infinity](https://clawhub.ai/user/tomasz-pedzierski-infinity)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workplace assistants use this skill to plan Polish leave requests, calculate business days against Polish holidays, and prepare leave-request forms for review or submission.

### Deployment Geography for Use:

Poland

## Known Risks and Mitigations:

Risk: The PDF path can automatically install an unpinned reportlab dependency at runtime.

Mitigation: Preinstall a pinned reportlab version through an approved setup process before enabling PDF generation.

Risk: The skill handles employee names, roles, departments, contact details, leave balances, and leave dates, and the documentation says employee data may be remembered.

Mitigation: Use only approved employee data and confirm where remembered data is stored and how it can be deleted.

Risk: Generated leave-request PDFs may contain personal data and can be written to local paths.

Mitigation: Restrict PDF output to an approved folder and review files before sharing or sending them.

Risk: The documentation describes sending leave requests by email.

Mitigation: Confirm the recipient and message contents before sending any leave request outside the local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomasz-pedzierski-infinity/skills/urlopnik)
- [Publisher profile](https://clawhub.ai/user/tomasz-pedzierski-infinity)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with optional generated PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local leave-request PDFs and may prompt for employee leave details.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
