## Description: <br>
Records daily work items in a local SQLite database and helps an agent correct entries, inspect history, and summarize daily or weekly progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanmwx](https://clawhub.ai/user/seanmwx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and individual contributors use this skill to keep a local work log, correct mistaken entries, review change history, and generate daily or weekly progress summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Work-history text is stored locally and may include sensitive details if the user provides them. <br>
Mitigation: Avoid logging secrets or highly confidential information, and choose separate database names or paths for different work contexts when needed. <br>
Risk: Replace, update, and delete operations can change the wrong work item if the target date or entry id is ambiguous. <br>
Mitigation: Resolve an explicit date or entry id from a day or week report before running commands that modify or remove records. <br>
Risk: Daily and weekly summaries can be incomplete when prior work was not recorded. <br>
Mitigation: Report only returned records and state clearly when a date has no recorded entries. <br>


## Reference(s): <br>
- [Work Progress Summary Pro on ClawHub](https://clawhub.ai/seanmwx/work-progress-summary) <br>
- [Command Reference](artifact/references/commands.md) <br>
- [Chat Reference](artifact/references/chat_reference.md) <br>
- [Chinese Output Templates](artifact/references/chinese_output.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text summaries with shell command invocations and JSON payloads where needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses explicit dates and local SQLite-backed records; supports concise Chinese response shapes when the user writes in Chinese.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
