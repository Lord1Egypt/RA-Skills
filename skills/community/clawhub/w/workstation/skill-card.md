## Description:

Create and SSH into cloud Linux servers with root access, instantly hosting websites on https://<name>.workstation.md via nginx on port 80.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renning22](https://clawhub.ai/user/renning22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent operators use this skill to provision temporary Linux workstations, connect over SSH, run commands as root, and publish web output behind a workstation.md URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent authority to install a global npm CLI, create or reuse SSH keys, provision a public internet server, and run commands as root.

Mitigation: Use a dedicated SSH key, require explicit approval before provisioning or publishing, prefer pinned package versions, and destroy the workstation when finished.

Risk: Public deployment and broad infrastructure access can expose unfinished services or sensitive files if commands are run without review.

Mitigation: Review proposed commands and deployed files before execution, restrict secrets from the workspace, and clean up public resources with the destroy command.

## Reference(s):

- [WORKSTATION.md ClawHub Skill](https://clawhub.ai/renning22/skills/workstation)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent through npm CLI installation, SSH key setup, workstation provisioning, SSH/SCP usage, web hosting, extension, listing, and teardown commands.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
