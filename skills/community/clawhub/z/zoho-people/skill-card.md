## Description:

Helps agents read and manage Zoho People HR records, forms, attendance, and leave through an authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and HR teams can ask an agent to retrieve or update specific employee, department, attendance, leave, and form records in their authorized Zoho People account. Developers can set up approved functions and triggers for related workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive employee and leave information may be accessed beyond the user's intended scope.

Mitigation: Confirm the account, connection, and exact records; access only records the user requests.

Risk: Writes to records or custom forms may change HR data unexpectedly.

Mitigation: Review the target and payload and obtain explicit approval before each write.

Risk: Hosted functions and persistent triggers can repeatedly process or send HR data.

Mitigation: Review function behavior and trigger destinations, and confirm automation before enabling it.

## Reference(s):

- [ClawHub zoho-people release](https://clawhub.ai/byungkyu/skills/zoho-people)
- [Maton](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Zoho People API overview](https://www.zoho.com/people/api/overview.html)
- [Zoho People forms API](https://www.zoho.com/people/api/forms-api/fetch-forms.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Natural-language responses with optional Markdown, code, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the authorized Zoho People connection and the records requested.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
