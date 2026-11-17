## Description:

Helps accounting teams extract invoice data, check authenticity, prepare reimbursement forms, and connect to approval workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fyniujin](https://clawhub.ai/user/fyniujin)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting staff use this skill to process Chinese invoices, review duplicate or anomalous claims, prepare reimbursement records, and route submissions through configured approval systems. A finance professional should review results before acting on them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial documents and generated records may contain sensitive information.

Mitigation: Review configuration, access controls, and local retention before processing documents.

Risk: Verification links and configured approval platforms can involve external services despite local processing of invoice files.

Mitigation: Confirm the destination and authorize external verification or approval connections before using them.

Risk: Approval credentials and scheduled reminders can create ongoing access or local background activity.

Mitigation: Keep API keys in environment variables and enable scheduled reminders only when a persistent local task is intended.

## Reference(s):

- [ClawHub release](https://clawhub.ai/fyniujin/skills/receipt-compliance)
- [Tax rules](artifact/references/tax-rules.md)
- [Setup guide](artifact/references/setup-guide.md)
- [Verification and approval integrations](artifact/references/api-endpoints.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, JSON, Files]

**Output Format:** [Markdown guidance, structured JSON, and generated reimbursement or review files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional Excel reports, vouchers, and HTML review pages depend on the requested workflow.]

## Skill Version(s):

4.5.0 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
