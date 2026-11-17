## Description:

Tyche Lite previews up to five invoices from a CSV, summarizes payment status, and drafts one friendly overdue-payment reminder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

External users, freelancers, and small businesses use this skill to preview invoice status from a small CSV file and generate a friendly reminder for an overdue invoice. It is intended as a lightweight invoice-review helper rather than a full receivables workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The provided dependency install command uses an overly broad system-package flag.

Mitigation: Install dependencies in a virtual environment and avoid running the command against system Python.

Risk: The skill includes visible upsell messaging and a Ko-fi purchase link.

Mitigation: Treat Tyche Pro and the purchase link as separate decisions from the invoice-preview task.

Risk: Invoice CSV content may include client names, emails, amounts, and payment status.

Mitigation: Review generated output before sharing it and avoid pasting sensitive invoice data into unrelated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/skills/tyche-lite)
- [ClawHub metadata homepage](https://clawhub.ai/occupythemilkyway/tyche-lite)
- [Publisher profile](https://clawhub.ai/user/occupythemilkyway)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads an optional invoice CSV through INVOICES_FILE and limits Lite previews to five invoices.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
