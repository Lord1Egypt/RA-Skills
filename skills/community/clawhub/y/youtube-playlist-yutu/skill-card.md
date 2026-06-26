## Description: <br>
Guides agents through listing, creating, updating, and deleting YouTube playlists with the yutu CLI, including first-time OAuth setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and channel operators use this skill to manage YouTube playlists from an agent-assisted shell workflow, including OAuth credential setup and yutu playlist commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The yutu CLI and OAuth token can access the user's YouTube account. <br>
Mitigation: Install only if the yutu CLI package is trusted and keep YouTube OAuth access scoped to the intended account. <br>
Risk: OAuth credential and token files may expose YouTube account access if shared or committed. <br>
Mitigation: Keep client_secret.json and youtube.token.json private, out of source control, and out of shared workspaces. <br>
Risk: Playlist creation, privacy changes, updates, or deletion can affect public channel content. <br>
Mitigation: Require explicit confirmation before creating public playlists, changing privacy settings, or deleting playlist IDs. <br>


## Reference(s): <br>
- [Yutu homepage](https://github.com/eat-pray-ai/yutu) <br>
- [Yutu setup guide](references/setup.md) <br>
- [Playlist list reference](references/playlist-list.md) <br>
- [Playlist insert reference](references/playlist-insert.md) <br>
- [Playlist update reference](references/playlist-update.md) <br>
- [Playlist delete reference](references/playlist-delete.md) <br>
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI flag tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference yutu CLI output formats such as table, JSON, YAML, or silent mode.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
