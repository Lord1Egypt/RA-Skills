## Description: <br>
Smart Ledger tracks personal income and expenses from Chinese or English natural-language notes, classifies transactions, and generates daily, weekly, monthly, and trend reports from local JSON data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dyby99-gif](https://clawhub.ai/user/dyby99-gif) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Individuals and agents supporting personal finance management use Smart Ledger to record income and expenses from natural-language notes, classify records, review summaries, and generate daily, weekly, monthly, and trend reports while keeping data local. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal finance notes, income, spending amounts, and raw transaction text are stored in a local JSON file. <br>
Mitigation: Install only when local storage of this data is acceptable, keep the file under the user's account, and back up ~/.openclaw/workspace/data/expenses/expenses.json if the records matter. <br>
Risk: Deleting a record by ID is immediate. <br>
Mitigation: Double-check record IDs before deletion and keep a current backup before removing important records. <br>
Risk: Natural-language parsing and keyword classification can misread amounts, dates, transaction type, or category. <br>
Mitigation: Review created records and reports before relying on them, and refine notes or category keywords when classification is inaccurate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dyby99-gif/smart-ledger) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text reports, JSON records or reports, and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores and edits records in a local JSON file at ~/.openclaw/workspace/data/expenses/expenses.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
