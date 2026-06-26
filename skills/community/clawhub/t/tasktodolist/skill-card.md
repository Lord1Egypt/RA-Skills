## Description: <br>
Manage multiple independent to-do lists with commands to add, list, complete, remove, clear tasks, and manage task lists by name. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guiguihao](https://clawhub.ai/user/guiguihao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to manage local named to-do lists from the command line, including adding, listing, completing, removing, clearing, and deleting task lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted task-list names can create or delete files outside the documented ~/.tasktodolist folder. <br>
Mitigation: Use simple task names containing only letters, numbers, dashes, and underscores; avoid names with .., /, or backslashes. <br>
Risk: Todo items are saved in local files and may expose sensitive content to local users or backups. <br>
Mitigation: Do not store secrets, credentials, or other sensitive values in todo items. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guiguihao/tasktodolist) <br>
- [Publisher profile](https://clawhub.ai/user/guiguihao) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Plain text CLI output with local JSON task-list files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores task lists under ~/.tasktodolist; task names are used in local file names.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
