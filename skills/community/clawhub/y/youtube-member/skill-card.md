## Description: <br>
Manage YouTube channel members by guiding an agent to list channel member information with the yutu CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and channel operators use this skill to prepare yutu commands for listing YouTube channel members after configuring Google OAuth credentials and a cached token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on yutu access to YouTube account data through Google OAuth credentials and a cached token. <br>
Mitigation: Install only when that access is acceptable, grant the minimum needed account access, and revoke or rotate the OAuth token if access is no longer needed or files are exposed. <br>
Risk: OAuth credential files such as client_secret.json and youtube.token.json can expose account access if committed or shared. <br>
Mitigation: Keep credential and token files private, outside source control and shared folders, and follow the setup guide for local configuration. <br>


## Reference(s): <br>
- [YouTube Member skill page](https://clawhub.ai/OpenWaygate/youtube-member) <br>
- [Yutu project homepage](https://github.com/eat-pray-ai/yutu) <br>
- [Yutu README](https://github.com/eat-pray-ai/yutu#readme) <br>
- [Yutu releases](https://github.com/eat-pray-ai/yutu/releases/latest) <br>
- [Yutu Setup Guide](references/setup.md) <br>
- [Member List](references/member-list.md) <br>
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI flag references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces yutu member-listing commands and setup guidance; command output may be table, JSON, or YAML depending on yutu flags.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
