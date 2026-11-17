## Description:

QuickBooks Online automation for chart of accounts setup, bank rule configuration, recurring transaction templates, reconciliation workflows, and journal entry generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, accountants, bookkeepers, and finance operators use this skill to generate guided QuickBooks Online automation steps and code snippets for bookkeeping setup, transaction templates, reconciliation, reporting queries, and journal entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents toward live QuickBooks Online write operations that affect accounts, recurring transactions, and journal entries.

Mitigation: Use a QBO sandbox first and require explicit human approval before any production write.

Risk: QBO API credentials and refresh tokens grant powerful financial access if exposed.

Mitigation: Provide least-privilege credentials through secure secret storage and never paste or log tokens.

Risk: Generated bookkeeping or journal-entry guidance can be incorrect for a business context.

Mitigation: Have an accountant or authorized reviewer validate outputs before applying them to production books.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline Python, shell, CSV, and accounting templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires existing QuickBooks Online credentials and human review before production accounting writes.]

## Skill Version(s):

98.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
