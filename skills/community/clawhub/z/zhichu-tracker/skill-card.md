## Description: <br>
Smart Expense Tracker helps users record income and expenses from Chinese or English natural-language entries, categorize transactions, and generate daily, weekly, monthly, and trend reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dyby99-gif](https://clawhub.ai/user/dyby99-gif) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and personal finance agents use this skill to maintain local income and expense records, review spending by category, and generate budget and trend summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores personal income and expense records on local disk. <br>
Mitigation: Keep the workspace private, review local file permissions, and back up expenses.json when the records matter. <br>
Risk: Deleting a record by ID is immediate. <br>
Mitigation: Check the target record ID before running delete commands and keep a backup before bulk edits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dyby99-gif/zhichu-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [CLI text output, Markdown guidance, and optional JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores income and expense records locally as JSON under the OpenClaw workspace data directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
