## Description: <br>
Manage YouTube playlist items through yutu CLI commands for listing, adding, updating, and deleting playlist entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and YouTube channel operators use this skill to have an agent prepare yutu commands for listing playlist items, inserting new playlist entries, updating metadata or privacy, and deleting playlist items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Google OAuth client secrets and cached YouTube tokens. <br>
Mitigation: Keep client_secret.json and youtube.token.json private, store them outside shared repositories when possible, and avoid exposing raw credentials in logs or shell history. <br>
Risk: Update and delete commands can change or remove playlist items. <br>
Mitigation: Verify playlist and playlist item IDs before running update or delete commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/OpenWaygate/youtube-playlist-item) <br>
- [yutu Homepage](https://github.com/eat-pray-ai/yutu) <br>
- [Yutu Setup Guide](references/setup.md) <br>
- [Playlist Item List](references/playlistItem-list.md) <br>
- [Playlist Item Insert](references/playlistItem-insert.md) <br>
- [Playlist Item Update](references/playlistItem-update.md) <br>
- [Playlist Item Delete](references/playlistItem-delete.md) <br>
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require the yutu CLI plus Google OAuth credential and cached token configuration.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
