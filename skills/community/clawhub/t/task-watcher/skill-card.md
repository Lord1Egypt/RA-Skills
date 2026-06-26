## Description: <br>
Task Watcher Skill monitors long-running asynchronous tasks and sends notifications when task states change or complete. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to register long-running tasks, poll their status through adapters, and receive notifications when state changes or terminal conditions occur. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores monitoring state under ~/.openclaw/shared-context and may create notification records for watched tasks. <br>
Mitigation: Confirm the local storage location is acceptable before installation and review stored task metadata for sensitive identifiers. <br>
Risk: Configured cron execution can periodically send notifications through the user's OpenClaw notification channel. <br>
Mitigation: Enable cron only after confirming the intended delivery channel and recipient, and review notification settings before deployment. <br>
Risk: Registered task metadata controls the local status paths and notification records processed by the watcher. <br>
Mitigation: Use simple task IDs and trusted task metadata when registering tasks. <br>


## Reference(s): <br>
- [ClawHub task-watcher release page](https://clawhub.ai/lanyasheng/task-watcher) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples; runtime notifications and JSON/JSONL task records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists monitoring state and notification records under ~/.openclaw/shared-context/monitor-tasks when configured.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
