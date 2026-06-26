## Description: <br>
Intelligent task management using workspace markdown files, with natural-language task CRUD, context-aware reminders, priority briefings, and weekly reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dgkim311](https://clawhub.ai/user/dgkim311) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual workspace users use this skill to manage personal work items as local markdown task files, including creating, updating, completing, querying, and reviewing tasks. It is intended for task and deadline tracking, not meeting scheduling or multi-collaborator project management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local tasks/ directory as persistent task memory, which may contain sensitive personal or work details. <br>
Mitigation: Install only when local task persistence is acceptable, and review stored task contents for sensitive information before sharing or archiving a workspace. <br>
Risk: Optional workspace integration can propose edits to AGENTS.md, SOUL.md, HEARTBEAT.md, or self-improving/tasks.md. <br>
Mitigation: Review and explicitly approve each proposed workspace integration change before applying it. <br>
Risk: Scheduled briefings and cleanup behavior may send task details through a configured messaging channel or move completed task files into archives. <br>
Mitigation: Check the cron channel, schedule, prompt behavior, and weekly archive cleanup settings before enabling scheduled jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dgkim311/smart-tasks) <br>
- [Context Window Management Strategy](artifact/references/context-strategy.md) <br>
- [Cron Job Templates](artifact/references/cron-templates.md) <br>
- [File Structure Reference](artifact/references/file-structure.md) <br>
- [Task File Format Reference](artifact/references/task-format.md) <br>
- [Workspace Integration](artifact/references/workspace-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with task-file templates and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local task markdown files and index metadata when the agent applies the workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
