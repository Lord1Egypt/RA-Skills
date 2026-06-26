## Description: <br>
Manage YouTube memberships levels by helping agents list channel membership-level information through the yutu CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and channel operators use this skill to prepare yutu CLI commands and setup guidance for listing YouTube channel membership levels from an authenticated account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth client secrets and cached YouTube tokens can expose account access if committed, shared, or logged. <br>
Mitigation: Keep client_secret.json and youtube.token.json out of git and shared folders, use private paths or a secret manager, and revoke or rotate credentials after suspected exposure. <br>
Risk: The skill depends on authenticated yutu CLI access to YouTube account data. <br>
Mitigation: Install only when OAuth access to the relevant YouTube account is acceptable and review commands before execution. <br>


## Reference(s): <br>
- [Memberships Level List](references/membershipsLevel-list.md) <br>
- [Yutu Setup Guide](references/setup.md) <br>
- [yutu project homepage](https://github.com/eat-pray-ai/yutu) <br>
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires yutu, Google Cloud OAuth client credentials, and a cached YouTube token.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
