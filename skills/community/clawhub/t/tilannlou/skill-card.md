## Description:

環境偵測 helps an agent produce local environment checking and management material for system tools, hardware, Python packages, Docker, networking, GPU monitoring, and Ollama/OpenClaw workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tilannlou](https://clawhub.ai/user/tilannlou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to recreate or generate local environment diagnostics and management scripts for AI development machines. It is most relevant when checking hardware, Python packages, Docker status, network ports, GPU state, and Ollama/OpenClaw setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated management script can persistently append Ollama environment variables to ~/.bashrc.

Mitigation: Review the shell changes before running them and remove the added ~/.bashrc lines if the configuration is no longer wanted.

Risk: The Docker maintenance flow can run an Ollama container with port 11434 exposed beyond localhost.

Mitigation: Bind the service to localhost when remote access is unnecessary and review firewall exposure before starting the container.

Risk: The Docker flow uses an unpinned Ollama image and a restartable container.

Mitigation: Pin the image to a reviewed version or digest and confirm the restart policy fits the host before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tilannlou/skills/tilannlou)
- [Publisher profile](https://clawhub.ai/user/tilannlou)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python and Bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated project structure, local scripts, command examples, and environment report formats.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
