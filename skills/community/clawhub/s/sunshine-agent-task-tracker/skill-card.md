## Description: <br>
Agent Task Tracker keeps a concise local task state file so an agent can resume requested work, running processes, progress, results, and next steps across session resets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to have an assistant maintain a compact markdown state snapshot for active work, background processes, completion status, and recovery after resets or compaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records task details and command context across sessions, which can expose sensitive information if secrets or private data are written to the task state file. <br>
Mitigation: Review memory/tasks.md periodically and avoid storing tokens, credentials, private user content, sensitive hostnames, or full commands containing secret arguments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sunshine-del-ux/sunshine-agent-task-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/Sunshine-del-ux) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Markdown task-state entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains memory/tasks.md as a concise state snapshot under 50 lines or 2KB, including active tasks, recent completions, background session details, notes, and results.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
