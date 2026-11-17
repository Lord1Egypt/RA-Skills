## Description:

Smart Ledger lets users record income and expenses from Chinese or English natural-language entries, auto-categorize transactions, and generate daily, weekly, monthly, and trend reports using local JSON storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyby99-gif](https://clawhub.ai/user/dyby99-gif)

### License/Terms of Use:

MIT

## Use Case:

External users and personal-finance users use this skill to track income and expenses, review category-level spending, and generate periodic budget reports from locally stored records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal finance records in a local JSON file.

Mitigation: Review local file access expectations before use and protect or back up ~/.openclaw/workspace/data/expenses/expenses.json according to the user's privacy needs.

Risk: Delete operations or manual bulk edits can remove or corrupt expense records.

Mitigation: Back up ~/.openclaw/workspace/data/expenses/expenses.json before using delete commands or editing records directly.

Risk: Natural-language parsing and keyword classification may misclassify transactions or miss amounts.

Mitigation: Review generated records and reports before relying on them for budgeting decisions, and update category keywords when classifications are inaccurate.

## Reference(s):

- [Smart Ledger on ClawHub](https://clawhub.ai/dyby99-gif/skills/smart-ledger)
- [Publisher Profile](https://clawhub.ai/user/dyby99-gif)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local expense records and reports under ~/.openclaw/workspace/data/expenses/expenses.json.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
