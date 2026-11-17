## Description:

Solo business management with dashboard, pipeline tracking, invoicing, and weekly reviews for clients, revenue, pipeline, invoices, and priorities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agistack](https://clawhub.ai/user/agistack)

### License/Terms of Use:

MIT-0

## Use Case:

Solo business operators and their agents use this skill to inspect local business metrics, track clients and pipeline status, draft invoices, prioritize work, and support weekly business reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles local client, revenue, invoice, pipeline, and priority data.

Mitigation: Keep the workspace memory directory local, review generated business records before reuse, and avoid sharing client or financial data outside the intended workspace.

Risk: The packaged release only includes the dashboard script, while the documentation describes additional invoice, pipeline, payment, priority, and review workflows.

Mitigation: Confirm required workflow scripts are present before relying on those workflows, and treat missing-script commands as unsupported until separately supplied.

Risk: The skill can draft invoices and track payments but is not a payment processor, tax filer, accountant, or legal adviser.

Mitigation: Use outputs as operational drafts and records only; route payments, tax decisions, and legal/accounting questions through appropriate external systems or professionals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agistack/skills/solopreneur)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Text and Markdown with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local workspace memory for client, revenue, invoice, pipeline, review, and priority data.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
