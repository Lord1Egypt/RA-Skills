## Description: <br>
Manage YouTube playlist images by guiding agents through yutu CLI commands to list, insert, update, and delete playlist images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and channel operators use this skill to manage YouTube playlist artwork through the yutu CLI, including setup guidance for OAuth credentials and token files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The yutu CLI uses OAuth credentials and cached tokens that can grant access to a YouTube account. <br>
Mitigation: Install yutu only from a trusted source and keep client_secret.json and youtube.token.json private. <br>
Risk: Update and delete commands can change or remove playlist images. <br>
Mitigation: Verify the active account, playlist IDs, and playlist image IDs before running content-changing commands. <br>
Risk: Insert commands can upload local images as public-facing playlist artwork. <br>
Mitigation: Review local image contents before upload and avoid using sensitive files as playlist images. <br>


## Reference(s): <br>
- [Yutu homepage](https://github.com/eat-pray-ai/yutu) <br>
- [YouTube Playlist Image on ClawHub](https://clawhub.ai/OpenWaygate/youtube-playlist-image) <br>
- [Setup guide](references/setup.md) <br>
- [Playlist Image List](references/playlistImage-list.md) <br>
- [Playlist Image Insert](references/playlistImage-insert.md) <br>
- [Playlist Image Update](references/playlistImage-update.md) <br>
- [Playlist Image Delete](references/playlistImage-delete.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and CLI flag tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may require yutu, Google OAuth credentials, and cached YouTube token files.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
