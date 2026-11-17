## Description:

Organizes receipts and expense records by period, category, and receipt completeness, with reminders for missing documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and finance-operations teams use this skill to prepare reimbursement materials, organize receipt lists, identify missing supporting documents, and produce reviewable submission notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receipt and reimbursement inputs may contain personal, financial, or sensitive business information.

Mitigation: Only provide files intended for expense organization, redact sensitive details when practical, and keep generated drafts within the appropriate finance review process.

Risk: Generated groupings, missing-document reminders, or submission notes may be incomplete or incorrect if the input records are incomplete.

Mitigation: Review the structured report before using it in any reimbursement or finance workflow and resolve listed confirmation items.

Risk: The optional --output path may create or overwrite a local report file.

Mitigation: Use stdout or --dry-run for review-first workflows, and choose an explicit output path when writing a file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/receipt-expense-sorter)
- [ClawHub publisher profile](https://clawhub.ai/user/52yuanchangxing)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Structured Markdown reports or JSON report objects, with optional file output when --output is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local draft/report generation for user-provided receipt and expense materials; no network access is indicated by the security evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
