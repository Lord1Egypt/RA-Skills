## Description:

Tyche generates invoice documents, payment status summaries, overdue reports, late-fee calculations, and reminder templates from a CSV of client billing records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers and small business users use this skill to turn a CSV of client invoices into ready-to-send invoice text, payment dashboards, overdue reports, and payment reminder drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill saves a Markdown report containing client and invoice details by default.

Mitigation: Run it from a private working directory and protect or delete generated invoice reports according to the user's data-handling requirements.

Risk: The install instructions use broad package installation flags.

Mitigation: Install dependencies in a virtual environment and avoid --break-system-packages.

Risk: The skill advertises a separate Tyche Pro package.

Mitigation: Review the separate tyche-pro package before installing it or providing any license key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/skills/tyche)
- [Tyche ClawHub homepage](https://clawhub.ai/occupythemilkyway/tyche)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with shell and Python code blocks; generated console summaries, invoice text, reminder drafts, and a local Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses optional environment variables for the invoice CSV path, sender details, currency, tax rate, late-fee rate, payment terms, and payment method.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
