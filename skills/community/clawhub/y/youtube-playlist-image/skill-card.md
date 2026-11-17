## Description:

Manage YouTube playlist images by listing, inserting, updating, or deleting playlist images through the yutu CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and channel operators use this skill to manage YouTube playlist imagery from an agent workflow. It provides guidance and shell commands for yutu setup and playlist image list, insert, update, and delete operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles YouTube OAuth credentials and cached tokens.

Mitigation: Protect client_secret.json and youtube.token.json with restrictive permissions, keep them out of git and shared folders, and install yutu only from trusted sources.

Risk: The skill can modify or delete YouTube playlist imagery.

Mitigation: Manually verify playlist IDs and playlist image IDs before running update or delete commands, especially when using content owner flags.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/openwaygate/skills/youtube-playlist-image)
- [yutu Project Homepage](https://github.com/eat-pray-ai/yutu)
- [Yutu Setup Guide](references/setup.md)
- [Playlist Image List](references/playlistImage-list.md)
- [Playlist Image Insert](references/playlistImage-insert.md)
- [Playlist Image Update](references/playlistImage-update.md)
- [Playlist Image Delete](references/playlistImage-delete.md)
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include yutu commands that call the YouTube API and may return table, JSON, YAML, or silent CLI output depending on selected flags.]

## Skill Version(s):

0.10.7-dev (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
