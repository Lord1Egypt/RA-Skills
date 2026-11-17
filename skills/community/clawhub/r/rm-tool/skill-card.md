## Description:

Remove files and directories permanently. Use for file deletion, cleanup, and disk space management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Rm Tool to let an agent remove files or directories during cleanup and disk space management workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can permanently remove files and folders, including recursively deleted directories.

Mitigation: Use explicit, narrow target paths; avoid broad globs and recursive force deletion unless the target has been verified.

Risk: The documented interactive option is not implemented by the included script.

Mitigation: Do not rely on interactive prompting for confirmation; review paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/rm-tool)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text command-line status and error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces irreversible file and directory deletion behavior when executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
