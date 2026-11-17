## Description:

Manage YouTube playlists by guiding an agent through yutu CLI commands to list, create, update, and delete playlists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to operate YouTube playlist workflows through the yutu CLI, including setup, listing playlists, creating new playlists, updating metadata, and deleting playlists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth client secrets and cached YouTube tokens can grant access to account or channel playlist data.

Mitigation: Keep client_secret.json and youtube.token.json private, avoid committing them to source control, and restrict access to the configured credential paths.

Risk: Delete and update commands can modify or remove playlists when run against the wrong account, channel, or playlist ID.

Mitigation: Check the authenticated account, channel, playlist IDs, and intended operation before allowing update or delete commands to run.

## Reference(s):

- [Yutu project homepage](https://github.com/eat-pray-ai/yutu)
- [Yutu README](https://github.com/eat-pray-ai/yutu#readme)
- [Yutu releases](https://github.com/eat-pray-ai/yutu/releases/latest)
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview)
- [Yutu Setup Guide](references/setup.md)
- [Playlist List](references/playlist-list.md)
- [Playlist Insert](references/playlist-insert.md)
- [Playlist Update](references/playlist-update.md)
- [Playlist Delete](references/playlist-delete.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with yutu CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yutu, Google OAuth credentials, and a cached YouTube token.]

## Skill Version(s):

0.10.7-dev (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
