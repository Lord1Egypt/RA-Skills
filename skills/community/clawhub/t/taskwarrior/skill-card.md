## Description: <br>
Workspace-local task management powered by Taskwarrior for adding, organizing, and tracking tasks by project, tags, due dates, and priority with data stored inside the active workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aghareza](https://clawhub.ai/user/aghareza) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to manage workspace-local Taskwarrior tasks, including adding, listing, modifying, completing, tagging, prioritizing, and annotating tasks while keeping task data inside the active workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Taskwarrior confirmations are disabled for automation, so broad edits, deletes, purges, or status changes can affect multiple tasks without an interactive prompt. <br>
Mitigation: Preview matching tasks before bulk changes, require explicit user intent for deletes or purges, and show a focused task info or filtered list after mutations. <br>
Risk: The skill depends on the external Taskwarrior binary being available in the runtime environment. <br>
Mitigation: Check task --version before use and ask the environment owner to install Taskwarrior in the base image if it is missing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aghareza/taskwarrior) <br>
- [Workspace Data Layout](references/workspace_data_layout.md) <br>
- [Taskwarrior Cheatsheet](references/taskwarrior_cheatsheet.md) <br>
- [Safe Command Policy](references/safe_command_policy.md) <br>
- [Examples](references/examples.md) <br>
- [ClawHub Notes](references/clawhub_notes.md) <br>
- [Taskwarrior Availability](references/install.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses workspace-local Taskwarrior paths and environment variables; does not install system packages at runtime.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
