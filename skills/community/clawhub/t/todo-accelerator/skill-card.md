## Description: <br>
Todo Accelerator helps users and agents capture, prioritize, process, and complete shared tasks through a local Obsidian-style Kanban board and companion notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liusining](https://clawhub.ai/user/liusining) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and agent operators use this skill to maintain a shared task queue where users can add tasks and agents can pick up, work on, and report progress on pending items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent heartbeat automation can cause an agent to pick up and work on saved tasks without fresh confirmation. <br>
Mitigation: Review and explicitly approve HEARTBEAT.md changes, keep heartbeat instructions narrow, and confirm specific tasks before targeted work. <br>
Risk: Task notes and boards may contain sensitive user requirements or work artifacts. <br>
Mitigation: Keep the board and notes in a dedicated folder, avoid storing secrets in task notes, and review note contents before sharing or committing them. <br>
Risk: Subagent delegation may route sensitive work to another agent when enabled on a task. <br>
Mitigation: Disable subagent delegation for sensitive work and review the allow-subagent and assigned-agent fields before processing a task. <br>


## Reference(s): <br>
- [Case Study: Todo Accelerator in Action](references/case-study.md) <br>
- [Note YAML Properties](references/note-yaml-properties.md) <br>
- [Processing the work-on-todo Output](references/processing-work-on-todo.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local Markdown task files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates a local Kanban board, companion notes, and a workspace configuration file.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
