## Description: <br>
Todos manages local to-do items by adding, completing, listing, and deleting tasks stored in a local JSON file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[radiantbk](https://clawhub.ai/user/radiantbk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to maintain a simple local task list, including adding tasks, marking them complete, viewing current or historical tasks, and deleting entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Todo titles and task details are saved on disk until deleted. <br>
Mitigation: Avoid storing passwords, tokens, or highly sensitive information in todo entries. <br>
Risk: Delete commands remove local todo entries from the JSON data file. <br>
Mitigation: Review destructive delete commands before running them. <br>


## Reference(s): <br>
- [Todos ClawHub release page](https://clawhub.ai/radiantbk/todos) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Plain text CLI output with local JSON file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores todo data in ~/.openclaw/workspace/memory/todos.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
