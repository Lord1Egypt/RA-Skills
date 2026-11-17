## Description:

Manage YouTube playlist items by guiding an agent through yutu CLI commands to list, insert, update, and delete playlist entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage YouTube playlist items from an agent workflow after configuring yutu with Google OAuth credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned third-party yutu CLI that handles OAuth credentials.

Mitigation: Use a trusted, pinned yutu version where possible, install with least privilege, and avoid running it as root or administrator.

Risk: OAuth client secrets and cached tokens can be exposed if client_secret.json or youtube.token.json are shared or committed.

Mitigation: Keep credential and token files out of shared locations and source control, and treat YUTU_CREDENTIAL and YUTU_CACHE_TOKEN values as secrets.

Risk: Update and delete commands can change or remove YouTube playlist data.

Mitigation: Double-check playlist IDs and playlist item IDs before running update or delete commands.

## Reference(s):

- [Setup Guide](references/setup.md)
- [Playlist Item Delete](references/playlistItem-delete.md)
- [Playlist Item Insert](references/playlistItem-insert.md)
- [Playlist Item List](references/playlistItem-list.md)
- [Playlist Item Update](references/playlistItem-update.md)
- [yutu project homepage](https://github.com/eat-pray-ai/yutu)
- [yutu README](https://github.com/eat-pray-ai/yutu#readme)
- [yutu releases](https://github.com/eat-pray-ai/yutu/releases/latest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include yutu command examples, required flags, optional output formats, OAuth setup guidance, and playlist item identifiers supplied by the user.]

## Skill Version(s):

0.10.7-dev (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
