## Description: <br>
Revolution Auto-Evolution orchestrates autonomous multi-agent review, execution, and audit loops over local task files so agents can break down goals, process one subtask per tick, and package completed work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate autonomous task execution through reviewer, executor, and auditor roles. It is intended for local task-file workflows where work is split into subtasks, advanced one heartbeat at a time, and checked before and after execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring autonomous agent work can change local files and package skills without enough human review. <br>
Mitigation: Use an isolated workspace, keep version-control backups, and require manual approval for destructive, credentialed, publishing, or production-impacting actions. <br>
Risk: Task files and generated role prompts may cause agents to perform unintended work if they are not reviewed. <br>
Mitigation: Review every task file and generated review, execution, and audit prompt before enabling heartbeat or cron execution. <br>
Risk: Heartbeat or cron operation can repeatedly advance tasks beyond the operator's intended scope. <br>
Mitigation: Run the coordinator with explicit task directories and monitor runs, and disable scheduled execution until task scope and acceptance criteria are confirmed. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [Task Example](references/task-example.json) <br>
- [Task Schema](config/task-schema.json) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, JSON task files, and generated role prompts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local task JSON files and emits phase-specific review, execution, and audit prompts for agent orchestration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata lists 0.5.7 and SKILL.md lists 0.6.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
