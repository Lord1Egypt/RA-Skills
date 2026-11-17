## Description:

A skill to execute SSH commands on remote servers, supporting both password and key-based authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xlbbb-cn](https://clawhub.ai/user/xlbbb-cn)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run a single approved command on a remote server over SSH and review the resulting stdout, stderr, and exit status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Arbitrary remote command execution can affect systems outside the local agent environment.

Mitigation: Run only explicit user-approved commands against intended hosts, and use least-privilege SSH accounts.

Risk: Unsafe SSH defaults and credential handling can expose systems or secrets.

Mitigation: Use verified host keys with --strict-host-key, avoid passing passwords or key passphrases on the command line, and avoid sensitive command output.

Risk: Command logs may expose secrets or operational data.

Mitigation: Review logged output before sharing or storing it, and avoid commands that print credentials or sensitive configuration.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Text, Guidance]

**Output Format:** [Command-line execution output with logged stdout, stderr, and exit status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SSH host, username, command, and either password or private-key authentication.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
