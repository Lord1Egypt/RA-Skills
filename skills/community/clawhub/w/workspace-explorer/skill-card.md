## Description:

Securely share a workspace through a temporary browser-based VS Code environment for remote inspection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrbeandev](https://clawhub.ai/user/mrbeandev)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to expose a chosen workspace in a browser-based IDE when the owner needs temporary live access to inspect files, install IDE extensions, or review code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose the selected workspace through a public tunnel and remote IDE session.

Mitigation: Use it only with workspaces that do not contain sensitive repositories, secrets, credentials, or private data, and stop the session promptly after inspection.

Risk: The skill relies on remote code and downloaded binaries at run time.

Mitigation: Prefer reviewed versions that bundle code, pin exact dependency versions, and verify downloaded binaries with checksums or signatures before use.

Risk: A tunnel left active longer than intended can extend remote access to the workspace.

Mitigation: Use the status check and heartbeat behavior to monitor active sessions and remind the owner when a session has been running too long.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrbeandev/skills/workspace-explorer)
- [Publisher profile](https://clawhub.ai/user/mrbeandev)
- [Repository listed in skill artifact](https://github.com/mrbeandev/workspace-explorer)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a temporary public workspace URL and password when its referenced start script is run.]

## Skill Version(s):

1.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
