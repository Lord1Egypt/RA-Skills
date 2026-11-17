## Description:

Set or display file creation permission mask. Use for controlling default file permissions on new files and directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to ask an agent for umask commands and guidance when inspecting or configuring default file permissions for newly created files and directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script silently sets the process umask to 000 while displaying it, which can weaken default permissions for subsequently created files in that process.

Mitigation: Review before installing or executing; restore the previous mask after inspection and require an explicit validated mask before changing permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/umask-tool)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script prints a umask value but should be reviewed before use because security evidence reports that it silently sets the process umask to 000.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
