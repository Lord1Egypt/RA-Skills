## Description:

Run a single command on a remote Tailscale node via SSH without opening an interactive session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xejrax](https://clawhub.ai/user/xejrax)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to have an agent prepare or run one-off SSH commands against a configured Tailscale-accessible remote host without starting an interactive SSH session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to run commands on the chosen remote machine.

Mitigation: Install only for machines you control, and verify the target host, user, port, and command before use.

Risk: The script-piping example executes a local script on the remote system with the SSH user's privileges.

Mitigation: Review scripts before piping them over SSH and avoid privileged remote users unless required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xejrax/skills/ssh-exec)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an SSH binary and configured SSH access to a target host.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
