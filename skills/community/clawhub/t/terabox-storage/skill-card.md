## Description:

Manage TeraBox cloud storage operations including login, upload, download, share, and transfer using the terabox CLI tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arthurpatten](https://clawhub.ai/user/arthurpatten)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to manage TeraBox cloud files through CLI-guided login, upload, download, share, transfer, listing, search, and file operations. It is intended for explicit TeraBox requests and includes confirmation and sandbox path rules for file actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and update a local terabox executable and overwrite its own skill files from remote sources.

Mitigation: Use it only in environments where that persistence is acceptable, and prefer explicit, verified updates over silent auto-update behavior.

Risk: Command transcripts, config output, tokens, or share passwords could expose TeraBox account or shared-file access.

Mitigation: Avoid sharing config output or command transcripts containing tokens, authorization codes, share passwords, or download links.

Risk: Cloud file operations can overwrite, move, share, or download user data.

Mitigation: Require clear user intent and confirmation for ambiguous paths, existing destination files, sharing, and transfer actions before execution.

## Reference(s):

- [TeraBox Storage skill page](https://clawhub.ai/arthurpatten/skills/terabox-storage)
- [TeraBox CLI command reference](reference/terabox-commands.md)
- [Authentication guide](reference/authentication.md)
- [Usage examples](reference/examples.md)
- [Troubleshooting](reference/troubleshooting.md)
- [Beta notes](reference/notes.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command confirmations, login guidance, path validation guidance, and references to terabox JSON output options.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
