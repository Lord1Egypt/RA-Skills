## Description: <br>
Task Persistence provides task continuity, session snapshots, and gateway restart recovery for agents managing long-running work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangdaowan](https://clawhub.ai/user/yangdaowan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to register long-running tasks, inspect active work after gateway restarts, and recover or complete persisted tasks in an OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local JSON records can include task descriptions, checkpoint data, and session snapshot content supplied by the user or agent. <br>
Mitigation: Use only the intended workspace path, avoid snapshotting sensitive conversation data unless local storage is acceptable, and clean old snapshots when they are no longer needed. <br>
Risk: Recovery commands may resume or report stale task state after a restart. <br>
Mitigation: Review recovered task lists and suggestions before continuing work, then explicitly complete, pause, cancel, or re-register tasks as appropriate. <br>


## Reference(s): <br>
- [ClawHub release page for Task Persistence](https://clawhub.ai/yangdaowan/task-persistence) <br>
- [Publisher profile: yangdaowan](https://clawhub.ai/user/yangdaowan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local workspace files for task queues, completed and failed task records, session snapshots, and gateway state.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
