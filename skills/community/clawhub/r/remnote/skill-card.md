## Description:

Search, read, and write RemNote notes and personal knowledge base content via remnote-cli, with explicit confirmation required before mutating commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robert7](https://clawhub.ai/user/robert7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and manage a user's RemNote knowledge base from the command line. It supports read-only search and navigation by default, with create, update, tagging, child insertion, replacement, and journaling gated on an exact user confirmation phrase.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or align remnote-mcp-server through a global npm package, and the server evidence notes the install is unpinned by default.

Mitigation: Pin remnote-mcp-server to a reviewed exact version or same approved minor line and avoid admin-level global installs where possible.

Risk: Recovery steps may stop and restart a shared OpenClaw browser profile.

Mitigation: Require user confirmation before browser stop, start, or recovery actions that could affect an active session.

Risk: Mutating RemNote commands can create, update, replace, retag, or journal user content.

Mitigation: Keep read-only commands as the default and require the exact phrase confirm write in the same turn before any mutating command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robert7/skills/remnote)
- [remnote-mcp-server](https://github.com/robert7/remnote-mcp-server)
- [RemNote bridge marketplace install guide](https://github.com/robert7/remnote-mcp-bridge/blob/main/docs/guides/install-plugin-via-marketplace-beginner.md)
- [RemNote bridge local development guide](https://github.com/robert7/remnote-mcp-bridge/blob/main/docs/guides/development-run-plugin-locally.md)
- [remnote-cli command reference](https://github.com/robert7/remnote-mcp-server/blob/main/docs/guides/remnote-cli-command-reference.md)
- [RemNote](https://www.remnote.com/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and command output interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers JSON CLI output for navigation and text output for single-note summaries; mutating operations require same-turn confirm write.]

## Skill Version(s):

0.16.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
