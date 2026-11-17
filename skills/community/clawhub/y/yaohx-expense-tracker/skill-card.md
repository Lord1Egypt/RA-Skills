## Description:

Yaohx Expense Tracker helps an agent record local personal expenses from text or payment screenshots, query monthly spending, manage categories, delete records, and generate monthly spending reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaohx-star](https://clawhub.ai/user/yaohx-star)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill with an agent to maintain a local personal expense ledger, capture spending from natural-language notes or payment screenshots, and review monthly spending summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deleting financial records can remove a user's source-of-truth expense data if the wrong record is selected.

Mitigation: Ask the user to confirm the exact record identifier and visible expense details before running a deletion workflow.

Risk: The optional OCR path recommends installing an unpinned dependency.

Mitigation: Install OCR dependencies only in a controlled environment with pinned, trusted package versions.

Risk: The release evidence warns that expected supporting scripts may be missing from the installed package.

Mitigation: Verify the installed package includes the required scripts before relying on recording, OCR, listing, reporting, or deletion workflows.

## Reference(s):

- [Server-resolved GitHub source repository](https://github.com/yaohx-star/yaohx-expense-tracker)
- [ClawHub skill page](https://clawhub.ai/yaohx-star/skills/yaohx-expense-tracker)
- [Publisher profile](https://clawhub.ai/user/yaohx-star)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown with shell command examples and JSON-shaped script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local categories and monthly expense JSON files when the supporting scripts are present.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
