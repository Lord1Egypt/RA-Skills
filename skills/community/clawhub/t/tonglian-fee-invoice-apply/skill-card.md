## Description:

Helps employees process Tonglian card-processing fee invoice applications by reading customer statements, calculating prior-month fees, preparing fixed invoice spreadsheets, and drafting the confirmation email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shouqianba](https://clawhub.ai/user/shouqianba)

### License/Terms of Use:

MIT-0

## Use Case:

Employees use this skill to turn Tonglian fee statements into invoice application materials, collect only missing invoice details, and prepare an email for user-confirmed submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice applications can be incorrect if the recipient, attachments, month, amount, invoice type, or tax details are wrong.

Mitigation: Verify all invoice details and both attachments with the user before approving any email send.

Risk: Remembered customer settings or web-sourced tax details may be stale or inaccurate.

Mitigation: Use trusted invoice and tax details, and allow users to review or correct remembered preferences before reuse.

Risk: The artifact references fixed spreadsheet templates, but the evidence package contains only the skill definition.

Mitigation: Confirm that the required template files are supplied elsewhere before running the workflow, and work from copies rather than editing originals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shouqianba/skills/tonglian-fee-invoice-apply)

## Skill Output:

**Output Type(s):** [Analysis, Files, Guidance]

**Output Format:** [Markdown summaries, completed spreadsheet files, and email text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before sending; expected file outputs are the fee receivables detail workbook and the Tonglian invoice application workbook.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
