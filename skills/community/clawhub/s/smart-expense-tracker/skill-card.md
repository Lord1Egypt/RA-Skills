## Description:

Expense Tracker helps an agent log local expense and income records, manage budgets and savings goals, generate finance summaries, split bills, track recurring payments, and export CSV reports from natural-language prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkpareek0315](https://clawhub.ai/user/mkpareek0315)

### License/Terms of Use:


## Use Case:

External users use this skill as a chat-based personal finance assistant for logging expenses and income, tracking budgets and savings goals, reviewing spending reports, and exporting local financial records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation phrases may cause unintended creation or editing of local financial files.

Mitigation: Use explicit finance-related prompts when invoking the skill and review local changes if it activates unexpectedly.

Risk: The skill creates and retains local personal finance data under ~/.openclaw/expense-tracker/.

Mitigation: Install only when local retention is acceptable, and periodically review, back up, export, or remove that directory according to user preference.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mkpareek0315/skills/smart-expense-tracker)
- [Publisher profile](https://clawhub.ai/user/mkpareek0315)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration, Guidance]

**Output Format:** [Markdown and plain text with JSON, CSV, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local files under ~/.openclaw/expense-tracker/ when activated.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
