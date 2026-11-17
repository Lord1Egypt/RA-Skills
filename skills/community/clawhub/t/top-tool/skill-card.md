## Description:

Display real-time view of running processes. Use for system monitoring, performance debugging, and resource management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system operators use this skill to inspect running processes while monitoring performance or investigating resource usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local process command lines may contain sensitive arguments and can be displayed by the tool.

Mitigation: Use the skill only in environments where exposing process command lines is acceptable, and avoid running it where secrets are passed as command arguments.

Risk: The documented filtering, sorting, batch, and resource-percentage options are not implemented by the bundled script.

Mitigation: Validate observed behavior before relying on the tool for filtered monitoring, sorted output, or CPU and memory percentage reporting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/top-tool)
- [Publisher profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text process listing and markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script prints PID and command data from local /proc entries.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
