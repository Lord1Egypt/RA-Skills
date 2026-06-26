## Description: <br>
Smarter Task Planner helps agents create timestamped task folders, plan work in ordered steps, save checkpoints, and resume interrupted analysis, research, extraction, and document-generation tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hou0515](https://clawhub.ai/user/hou0515) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to structure multi-step work into workspace folders, preserve task memory, and recover unfinished work after interruptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper scripts persist task summaries and metadata in the OpenClaw workspace, which can retain sensitive user or project details. <br>
Mitigation: Avoid putting secrets, credentials, private customer data, or confidential source material in task notes or checkpoint summaries. <br>
Risk: The security evidence flags path-scoping and heartbeat script-location issues that can affect where files are read or written. <br>
Mitigation: Review or patch the heartbeat template before enabling automatic checks, and use only simple task IDs without slashes, absolute paths, or traversal segments. <br>
Risk: The skill can automatically create task folders and update memory files when its scripts are run. <br>
Mitigation: Install it only in workspaces where persistent task memory is desired, and review generated files before relying on them for recovery. <br>


## Reference(s): <br>
- [Smarter Task Planner ClawHub Page](https://clawhub.ai/hou0515/smarter-task-planner) <br>
- [Workflow Analysis Guide](references/workflow-analysis.md) <br>
- [Task Memory Guide](references/task-memory-guide.md) <br>
- [Workspace Structure Examples](references/examples.md) <br>
- [Heartbeat Guide](templates/HEARTBEAT-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Files, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and workspace file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates OpenClaw workspace task folders, memory files, and task metadata when its helper scripts are run.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
