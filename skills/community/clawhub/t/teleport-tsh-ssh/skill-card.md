## Description:

Use Teleport tsh CLI with a Machine ID (tbot) identity file to SSH into Teleport-managed hosts or run remote commands through Teleport access controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webvictim](https://clawhub.ai/user/webvictim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect to Teleport-managed SSH nodes, run remote commands, list available nodes, transfer files with tsh scp, and troubleshoot tsh access using a local tbot-refreshed Machine ID identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may discover and select a local Teleport identity file containing private key material.

Mitigation: Configure the exact identity path and require confirmation before using any discovered fallback identity.

Risk: The skill can guide remote command execution and file transfers through Teleport.

Mitigation: Require user confirmation before state-changing remote commands or file copies, and preserve stderr for audit and troubleshooting.

## Reference(s):

- [tsh ssh reference](references/tsh-ssh-reference.md)
- [Teleport tsh ssh documentation](https://goteleport.com/docs/reference/cli/tsh/#tsh-ssh)
- [ClawHub skill page](https://clawhub.ai/webvictim/skills/teleport-tsh-ssh)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown with inline bash command patterns and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prompt for an identity file path or Teleport proxy when required inputs are unavailable.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
