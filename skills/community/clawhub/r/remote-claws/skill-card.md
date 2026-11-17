## Description:

Full control of a remote machine via Remote Claws MCP: screenshots, mouse/keyboard, browser automation, run commands, read/write files on the remote host.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wentbackward](https://clawhub.ai/user/wentbackward)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use this skill to let an agent control a configured remote desktop through Remote Claws MCP for browser automation, desktop interaction, command execution, and remote file operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent can operate the configured remote machine beyond the user's intended scope.

Mitigation: Install only when remote machine operation is intended, and enforce least-privilege permissions.json policies with IP and host allowlists.

Risk: Bearer token exposure could allow unauthorized remote access.

Mitigation: Protect the bearer token and rotate it if exposure is suspected.

Risk: Command execution and remote file write, delete, or move actions can change system state or data.

Mitigation: Restrict these actions to the minimum required permissions and review high-impact operations before use.

Risk: Persisted browser sessions may let an agent act inside logged-in accounts.

Mitigation: Use dedicated browser profiles or accounts with limited privileges when granting browser access.

## Reference(s):

- [Remote Claws homepage](https://github.com/wentbackward/remote-claws)
- [Remote Claws OpenClaw setup guide](https://github.com/wentbackward/remote-claws/blob/master/remote-claws-openclaw-setup-guide.md)
- [Remote Claws security documentation](https://github.com/wentbackward/remote-claws#security)
- [ClawHub skill page](https://clawhub.ai/wentbackward/skills/remote-claws)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with MCP tool action names and command or configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides use of remote_browser, remote_desktop, remote_exec, and remote_files actions against the configured remote host.]

## Skill Version(s):

1.2.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
