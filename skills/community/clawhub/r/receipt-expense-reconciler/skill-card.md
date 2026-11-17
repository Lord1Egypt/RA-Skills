## Description:

Parse receipts and invoices, categorize spend, detect anomalies, and produce tax-ready expense summaries for freelancers and SMB operators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anugotta](https://clawhub.ai/user/anugotta)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers and SMB operators use this skill to turn receipt, invoice, and card-export data into reconciled expense records, category summaries, anomaly reports, and tax-preparation checklists. It supports operational accounting review, not legal or tax advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receipt, invoice, bank, and card exports may contain sensitive business or financial records.

Mitigation: Use the skill only with files intended to be shared with the agent, and review low-confidence or anomalous rows manually.

Risk: Expense summaries prepared for tax workflows can be incomplete, misclassified, or unsuitable for filing decisions.

Mitigation: Verify tax-ready outputs with a qualified accountant or tax advisor before filing.

## Reference(s):

- [Setup](setup.md)
- [Examples](examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown tables, summaries, review notes, and export checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include parsed record tables, category summaries, anomaly reports, and tax-ready export checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
