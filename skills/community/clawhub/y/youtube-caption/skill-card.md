## Description: <br>
Manage YouTube video captions by listing, inserting, updating, downloading, or deleting caption tracks with the yutu CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to manage caption tracks for YouTube videos, including setup, listing, insertion, update, download, and deletion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload, update, publish, or delete captions through the user's Google account. <br>
Mitigation: Confirm the Google account, video ID, caption ID, and local caption file before running insert, update, publish, or delete commands. <br>
Risk: OAuth credential and token files can grant access to YouTube API operations if exposed. <br>
Mitigation: Keep client_secret.json and youtube.token.json out of shared folders and source control. <br>
Risk: The workflow depends on the external yutu CLI and YouTube API credentials. <br>
Mitigation: Install yutu from trusted sources and grant only the YouTube access required for the intended caption workflow. <br>


## Reference(s): <br>
- [Yutu project homepage](https://github.com/eat-pray-ai/yutu) <br>
- [Yutu README](https://github.com/eat-pray-ai/yutu#readme) <br>
- [Yutu releases](https://github.com/eat-pray-ai/yutu/releases/latest) <br>
- [Yutu Setup Guide](references/setup.md) <br>
- [Caption Delete](references/caption-delete.md) <br>
- [Caption Download](references/caption-download.md) <br>
- [Caption Insert](references/caption-insert.md) <br>
- [Caption List](references/caption-list.md) <br>
- [Caption Update](references/caption-update.md) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and option tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local OAuth credential and token files required by yutu.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
