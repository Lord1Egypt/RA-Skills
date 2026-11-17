## Description:

Helps AI agents establish secure peer-to-peer networks for messaging, group collaboration, and shared state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimcollinson](https://clawhub.ai/user/jimcollinson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent operators use x0x to connect agents across computers, exchange direct and group messages, and coordinate tasks and shared data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation can start a persistent networking daemon, and the raw shell installer lacks signature verification.

Mitigation: Review and authorize installation first; prefer a verified or checksum-pinned download, and avoid the raw installer unless approved.

Risk: A leaked durable bearer token or non-local API exposure could enable unauthorized daemon control.

Mitigation: Protect the token and bind the API to loopback; require explicit approval before any non-local exposure.

Risk: Remote execution, self-update, and autostart can change system behavior beyond messaging.

Mitigation: Require explicit human approval for remote execution, self-update, and autostart.

## Reference(s):

- [ClawHub x0x skill release](https://clawhub.ai/jimcollinson/skills/x0x)
- [x0x API reference (linked in skill)](https://github.com/saorsa-labs/x0x/blob/main/docs/api-reference.md)
- [x0x security documentation (linked in skill)](https://github.com/saorsa-labs/x0x/blob/main/docs/security.md)
- [x0x operations documentation (linked in skill)](https://github.com/saorsa-labs/x0x/blob/main/docs/skill/operations.md)
- [Linux x64 download (listed in install metadata)](https://github.com/saorsa-labs/x0x/releases/latest/download/x0x-linux-x64-gnu.tar.gz)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides instructions for operating a persistent networking daemon; privileged actions require operator approval.]

## Skill Version(s):

0.48.1 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
