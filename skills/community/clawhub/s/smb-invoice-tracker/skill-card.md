## Description:

SMB Invoice Tracker helps freelancers and small businesses manually track invoices, review paid and outstanding status, generate cash flow reports, and optionally draft reminder text with MiniMax.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzargona](https://clawhub.ai/user/jzargona)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers and small-business operators use this skill through an agent to add invoices, review outstanding or paid status, produce cash-flow reports, and draft reminder messages for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice records are stored locally under ~/.openclaw/smb-invoice-tracker and may be visible to other users on shared systems if filesystem permissions are loose.

Mitigation: Use the skill only on trusted machines and restrict permissions on the invoice tracker directory when storing business invoice data.

Risk: Optional LLM reminder generation sends payer, amount, due date, and note fields to the MiniMax API.

Mitigation: Do not generate LLM reminders for sensitive invoices unless that data sharing is acceptable; review generated reminder text before sending it manually.

Risk: Gmail scanning, WhatsApp reminders, Stripe payment detection, Telegram digests, and CSV export are not implemented in this release.

Mitigation: Treat this release as a manual local invoice tracker and do not rely on it for automated collection, payment reconciliation, or messaging workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jzargona/skills/smb-invoice-tracker)
- [Reference docs](references/README.md)
- [Marketplace listing copy](references/marketing.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Plain-text CLI output, local JSON ledger files, and optional reminder text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores invoice and configuration data locally under ~/.openclaw/smb-invoice-tracker; optional reminder generation sends invoice fields to MiniMax only when MINIMAX_API_KEY is set.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
