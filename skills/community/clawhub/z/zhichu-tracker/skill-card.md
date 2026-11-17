## Description:

Smart Expense Tracker helps agents record income and expenses from natural-language entries, classify transactions, and generate day, week, month, and trend reports from local JSON data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyby99-gif](https://clawhub.ai/user/dyby99-gif)

### License/Terms of Use:

MIT

## Use Case:

Individuals and agents use this skill to keep local personal finance records, summarize recent spending, and produce CNY-oriented reports. It is most useful for Chinese natural-language expense tracking and budget review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal finance records are stored locally, and deleting a record is permanent.

Mitigation: Back up ~/.openclaw/workspace/data/expenses/expenses.json before deleting records or making large edits.

Risk: The tracker is oriented around Chinese natural-language entries and CNY reporting, so unsupported wording or currencies may be parsed or categorized incorrectly.

Mitigation: Review records and reports before relying on them, and adjust category keywords in artifact/assets/categories.json for the user's spending vocabulary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dyby99-gif/skills/zhichu-tracker)
- [Publisher profile](https://clawhub.ai/user/dyby99-gif)
- [SKILL.md](artifact/SKILL.md)
- [Category configuration](artifact/assets/categories.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [CLI text or JSON reports with natural-language accounting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores and reads local JSON records under ~/.openclaw/workspace/data/expenses; report commands can emit text or JSON.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
