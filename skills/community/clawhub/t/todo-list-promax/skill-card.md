## Description: <br>
Todo List Promax helps an agent capture personal tasks from chat messages and attachments, classify them, manage completion or deletion, and remind the user about unfinished dated tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z-zihan](https://clawhub.ai/user/z-zihan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to maintain a local personal todo list from natural-language chat, including task capture, lookup, completion, deletion confirmation, modification, single-step undo, attachment handling, and daily reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently stores original task messages and attachments under the workspace, which may include secrets, private documents, credentials, or sensitive personal details. <br>
Mitigation: Use it only for non-sensitive todos, avoid attaching private files or credentials, and review the workspace todo-list directory before sharing or archiving the workspace. <br>
Risk: The security evidence notes conflicting English and Chinese instructions about whether raw source messages are shown in normal todo queries. <br>
Mitigation: Confirm the active language behavior before relying on query output, and treat stored source messages as potentially visible until the publisher aligns the instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/z-zihan/todo-list-promax) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown tables, plain-language confirmations, reminder text, JSON-backed todo records, and cron setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist todo records, original source messages, attachments, backups, and cleanup logs under the workspace.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
