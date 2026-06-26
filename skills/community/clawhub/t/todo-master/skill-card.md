## Description: <br>
待办大师 helps agents manage local todos through a Python CLI backed by SQLite, including initialization, add, list, show, update, complete, reopen, archive, statistics, and migration support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Asir-zhang](https://clawhub.ai/user/Asir-zhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to keep local personal or workflow todos without relying on an online service. It is intended for user-directed task creation, querying, status updates, archiving, and local persistence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Todo titles and content are stored locally on disk. <br>
Mitigation: Choose the data directory deliberately and avoid putting secrets in todo entries. <br>
Risk: State-changing commands can alter todo records. <br>
Mitigation: Keep add, update, done, reopen, and archive commands user-directed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Asir-zhang/todo-master) <br>
- [OpenClaw Todo Skill introduction](references/INTRO.md) <br>
- [OpenClaw Todo Skill technical design](references/TECH_SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and CLI-oriented text with optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local filesystem and SQLite state after explicit initialization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
