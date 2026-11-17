## Description:

Workspace Organizer helps agents create timestamped task folders, save progress memories, and recover unfinished sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hou0515](https://clawhub.ai/user/hou0515)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to structure workspace output folders, record task checkpoints, and resume unfinished work from local task metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File-writing scripts may let unsafe task or step names escape the intended task area or corrupt recovery data.

Mitigation: Use only trusted, simple task and step names; avoid slashes, backslashes, drive prefixes, and '..'; review generated paths before running write operations.

Risk: The PowerShell fallback has unresolved path containment and metadata preservation concerns.

Mitigation: Prefer the Python scripts and avoid the PowerShell fallback until those issues are fixed and reviewed.

Risk: Heartbeat recovery checks can create recurring task scans and recovery prompts.

Mitigation: Enable the heartbeat template only when recurring recovery checks are desired.

## Reference(s):

- [Workspace structure examples](references/examples.md)
- [Task memory guide](references/task-memory-guide.md)
- [Workflow analysis guide](references/workflow-analysis.md)
- [Heartbeat recovery guide](templates/HEARTBEAT-guide.md)
- [ClawHub skill page](https://clawhub.ai/hou0515/skills/workspace-organizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and local workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write daily memory Markdown, long-term memory Markdown, task metadata JSON, and timestamped task folders when helper scripts are run.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
