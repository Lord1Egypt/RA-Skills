## Description: <br>
Manage YouTube channels by guiding agents to list channel information or update channel metadata with the yutu CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and channel operators use this skill to prepare yutu commands for viewing owned or specified YouTube channels and updating channel metadata such as title, description, country, custom URL, and default language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses OAuth client secrets and cached YouTube tokens to access a user's YouTube account. <br>
Mitigation: Keep client_secret.json and youtube.token.json out of repositories and shared folders, and provide credentials only from trusted local paths or environment variables. <br>
Risk: Channel update commands can change live YouTube channel metadata. <br>
Mitigation: Review the target channel ID and all proposed title, description, country, custom URL, and language values before running any update command. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/OpenWaygate/youtube-channel) <br>
- [yutu Project Homepage](https://github.com/eat-pray-ai/yutu) <br>
- [yutu README](https://github.com/eat-pray-ai/yutu#readme) <br>
- [Yutu Setup Guide](references/setup.md) <br>
- [Channel List](references/channel-list.md) <br>
- [Channel Update](references/channel-update.md) <br>
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and command options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires yutu, OAuth credentials, and a cached YouTube token; update commands can modify live channel metadata.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
