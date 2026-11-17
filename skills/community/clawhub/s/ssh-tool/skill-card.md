## Description:

Securely connect to remote systems via the SSH protocol. Use for remote server management, file transfer, and tunneling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect to remote systems for command execution, file transfer, and SSH port forwarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted or malformed host values may be interpreted as local SSH options, expanding the authority of agent-driven SSH use.

Mitigation: Reject leading-dash hosts, validate SSH destinations, and allow only explicitly approved SSH options before deployment.

Risk: The skill can initiate remote command execution, file transfer, and port forwarding without clearly scoped destination authority.

Mitigation: Require human review of allowed hosts, commands, file transfer paths, and tunnel options before using the skill in automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/ssh-tool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SSH connection targets, remote commands, file transfer guidance, and port forwarding options.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
