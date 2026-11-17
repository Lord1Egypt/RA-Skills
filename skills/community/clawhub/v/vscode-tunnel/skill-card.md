## Description:

Start VS Code Remote Tunnel in Docker containers for remote terminal access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[listky](https://clawhub.ai/user/listky)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to start, stop, inspect, and log a VS Code Remote Tunnel from a Linux Docker container when they need remote terminal access through VS Code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A running VS Code Remote Tunnel can provide remote terminal access to the container after Microsoft authorization.

Mitigation: Use the skill only in an intentionally exposed, low-privilege container; start the tunnel only on explicit request and stop it when the session is finished.

Risk: The skill downloads and runs the VS Code CLI without strong integrity verification.

Mitigation: Review the downloaded CLI source and add integrity verification before relying on this skill in higher-trust environments.

## Reference(s):

- [VS Code CLI stable Alpine x64 download endpoint](https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command usage, environment variables, tunnel status, logs, and Microsoft authorization instructions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
