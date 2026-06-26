## Description: <br>
Synchronize TickTick (Dida) and Google Tasks bidirectionally, including list/project mapping, task content sync, completion sync, and smart-list export (Today, Next 7 Days, All). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JP1222](https://clawhub.ai/user/JP1222) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to set up, run, schedule, and troubleshoot bidirectional synchronization between TickTick and Google Tasks while preserving list mappings, task content, completion state, priority markers, and smart-list exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sync can automatically change or delete live Google Tasks and TickTick data, including when scheduled. <br>
Mitigation: Test first with non-critical lists or accounts, back up important tasks, and enable cron only after reviewing sync_db.json and sync_log.json. <br>
Risk: OAuth token files provide write access to both task services. <br>
Mitigation: Protect Google and TickTick token files, store them only in the configured private paths, and rotate or re-authorize credentials if exposure is suspected. <br>


## Reference(s): <br>
- [Task Sync on ClawHub](https://clawhub.ai/JP1222/task-sync) <br>
- [Google Tasks REST API](https://developers.google.com/workspace/tasks/reference/rest) <br>
- [TickTick Open API](https://developer.ticktick.com/) <br>
- [OpenClaw](https://openclaw.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to run OAuth setup scripts, execute sync.py, inspect sync_db.json and sync_log.json, or configure scheduled execution.] <br>

## Skill Version(s): <br>
2.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
