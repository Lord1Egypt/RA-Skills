## Description: <br>
Enables OpenClaw agents to autonomously execute prioritized tasks on a heartbeat loop with logging, auditing, error handling, and workspace hygiene. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[casperzinou](https://clawhub.ai/user/casperzinou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to run a recurring autonomous task queue with state tracking, heartbeat-driven execution, logs, self-audits, and workspace hygiene controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent autonomous execution can repeatedly act on queued tasks with broad workspace effects. <br>
Mitigation: Install only in a tightly scoped workspace, keep TASKS.md limited to low-risk tasks, and require human approval for public posting, account actions, financial or business data changes, and other high-impact actions. <br>
Risk: Workspace hygiene behavior can move, truncate, clean, or archive project files and logs. <br>
Mitigation: Disable or require approval for hygiene actions, protect important logs and project files, and review archive and cleanup behavior before enabling scheduled heartbeats. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/casperzinou/talonforge-god-mode) <br>
- [HEARTBEAT-template.md](references/HEARTBEAT-template.md) <br>
- [TASKS-template.md](references/TASKS-template.md) <br>
- [god-mode-state-template.json](references/god-mode-state-template.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell setup commands and JSON state templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates workspace task, heartbeat, state, memory, and archive files when installed and run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
