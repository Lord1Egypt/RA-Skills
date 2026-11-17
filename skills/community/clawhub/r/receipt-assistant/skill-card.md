## Description:

Receipt Assistant helps agents process reimbursement receipts by identifying supported receipt types, extracting key fields, renaming files, and generating summary reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yy-c8](https://clawhub.ai/user/yy-c8)

### License/Terms of Use:


## Use Case:

Employees and agents use this skill to organize reimbursement receipts, including train tickets, taxi receipts, itinerary receipts, and hotel invoices. It supports folder scanning, receipt-field extraction, standardized file naming, first-run configuration, and Excel summary report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receipt-derived filenames and output paths can write outside the intended output folder if untrusted values are not constrained.

Mitigation: Use only trusted receipt folders, set a dedicated output directory, avoid elevated privileges, and add filename sanitization plus output-directory confinement checks before deployment.

Risk: Generated spreadsheets may contain untrusted receipt data that can create risky Excel content.

Mitigation: Treat generated spreadsheets as untrusted until reviewed and neutralize formula-like cell values before writing Excel files.

Risk: Dependencies are specified with minimum versions rather than pinned versions.

Mitigation: Pin and review dependencies before installation in production or shared environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yy-c8/skills/receipt-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON extraction prompts, Python helper outputs, renamed receipt files, and Excel report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured company name, default person name, output directory, and receipt-specific naming rules.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
