## Description:

Checks the health of a Docker-based Linux VM over SSH and reports system resources, disk usage, container status, database sizes, and cleanup opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonylnng](https://clawhub.ai/user/tonylnng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run post-deploy sanity checks on Docker-based Linux servers, identify resource pressure, review database and container usage, and find cleanup opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe SSH argument construction and disabled host-key verification can expose remote host access to spoofing or malformed connection parameters.

Mitigation: Quote and validate SSH inputs, avoid shell-interpolated SSH command strings, and restore host-key verification before use.

Risk: The skill stores VM host, username, and SSH key path in TOOLS.md, which can expose connection metadata if the file is shared or committed.

Mitigation: Keep TOOLS.md local, restrict file access, and avoid storing secrets or committing connection metadata.

Risk: Cleanup commands can remove unused Docker images, build cache, and stopped containers on the remote host.

Mitigation: Require explicit user confirmation, review the target host and cleanup scope, and avoid broad Docker prune operations unless approved.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with shell command output and health-check findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist VM host, username, and SSH key path in TOOLS.md during first-time configuration.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
