## Description:

Set up and maintain Raspberry Pi avoiding common hardware and configuration pitfalls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, makers, and operators use this skill for practical Raspberry Pi setup, maintenance, and troubleshooting guidance across power, storage, GPIO, networking, Docker, and headless operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Docker installation guidance recommends piping a remote installer script directly to a shell.

Mitigation: Prefer Docker's signed package repository instructions, or download, inspect, and verify the installer before execution.

Risk: Applying Raspberry Pi power, storage, GPIO, networking, or SSH guidance incorrectly can cause device instability, data loss, hardware damage, or exposed remote access.

Mitigation: Review settings and commands against the target Raspberry Pi model, connected hardware, and network policy before applying them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/raspberry)
- [Docker Convenience Installer](https://get.docker.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise checklist-style operational advice for Raspberry Pi setup and maintenance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
