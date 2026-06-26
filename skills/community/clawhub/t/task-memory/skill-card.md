## Description: <br>
Task Memory helps an agent persistently register, check, update, complete, archive, and purge long-running tasks so commitments are not forgotten across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huyaohuahk](https://clawhub.ai/user/huyaohuahk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep long-running commitments in a JSON task store, check deadlines at session start or heartbeat time, and mark tasks done, removed, archived, or purged. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores durable task data that may include personal, business, or financial details. <br>
Mitigation: Avoid sensitive details in task titles or notes and clear the bundled todo.json before installation. <br>
Risk: The task manager script uses an unexpected hard-coded write path. <br>
Mitigation: Change the task database path to a user-owned skill directory before enabling the skill. <br>
Risk: Heartbeat checks and QQ/IM reminders can send task content outside the local workspace. <br>
Mitigation: Enable reminder integrations only after deciding what data may be stored or sent. <br>
Risk: The artifact includes active finance-related task records. <br>
Mitigation: Remove bundled task records before deployment and start with an empty task database. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/huyaohuahk/task-memory) <br>
- [Task Memory Changelog](references/CHANGELOG.md) <br>
- [Task Database Template](references/todo.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON task records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local todo.json task database and archive completed tasks for 30 days.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and changelog, released 2026-04-01) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
