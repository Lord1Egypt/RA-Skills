## Description: <br>
Manage YouTube search by helping an agent search videos, channels, playlists, and other YouTube resources through the yutu CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content workflows use this skill to let an agent run YouTube searches, filter results, and return video, channel, playlist, or resource listings through yutu. It is useful when an agent needs YouTube search results with controllable CLI flags and output formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on Google OAuth credential and cached token files that can grant YouTube API access if exposed. <br>
Mitigation: Store client_secret.json and youtube.token.json privately, do not commit or share them, and revoke or rotate the Google OAuth credentials if either file is exposed. <br>
Risk: The yutu CLI package and repository are third-party dependencies. <br>
Mitigation: Install only after trusting the yutu package publisher and repository, and prefer pinned or reviewed package versions in controlled environments. <br>


## Reference(s): <br>
- [YouTube Search on ClawHub](https://clawhub.ai/OpenWaygate/youtube-search-yutu) <br>
- [yutu GitHub repository](https://github.com/eat-pray-ai/yutu) <br>
- [Search List](references/search-list.md) <br>
- [Yutu Setup Guide](references/setup.md) <br>
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; yutu search results may be returned as table, JSON, or YAML depending on the CLI flags used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the yutu binary plus Google OAuth credential and cached token files before YouTube API searches can run.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
