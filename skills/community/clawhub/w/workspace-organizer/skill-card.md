## Description: <br>
Organizes task files and memory for OpenClaw workspaces by creating timestamped task folders and supporting session recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hou0515](https://clawhub.ai/user/hou0515) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to structure task workspaces, save local progress notes, and recover unfinished task context across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task notes and recovery metadata may contain sensitive workspace context. <br>
Mitigation: Avoid putting secrets in task notes and review saved memory before reusing old context. <br>
Risk: Periodic recovery checks may surface stale or sensitive unfinished task context. <br>
Mitigation: Review the heartbeat template before enabling periodic checks and prefer manual recovery for sensitive work. <br>
Risk: The skill writes local task memory and recovery metadata into the workspace. <br>
Mitigation: Install it only when local task memory and recovery metadata are desired for the workspace. <br>


## Reference(s): <br>
- [Task Memory Guide](references/task-memory-guide.md) <br>
- [Workflow Analysis](references/workflow-analysis.md) <br>
- [Workspace Structure Examples](references/examples.md) <br>
- [Heartbeat Recovery Guide](templates/HEARTBEAT-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and script-backed workspace file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local task folders, memory notes, task metadata, and recovery prompts when its scripts are used.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
