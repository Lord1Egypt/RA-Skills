## Description: <br>
Manage YouTube Super Chat events by helping an agent list Super Chat events for a channel through the yutu CLI, with setup and installation guidance for first-time users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install and configure yutu, authenticate with YouTube API OAuth credentials, and list YouTube Super Chat events for a channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on OAuth client secrets, cached YouTube tokens, and YUTU_* credential values that can grant access to the selected YouTube account if exposed. <br>
Mitigation: Keep client_secret.json, youtube.token.json, and YUTU_* credential values private, do not commit them to source control, and revoke or rotate OAuth access if either file is exposed. <br>
Risk: The skill depends on the third-party yutu CLI to access YouTube APIs. <br>
Mitigation: Install only if you trust the yutu CLI and are comfortable granting it access to the selected YouTube account. <br>


## Reference(s): <br>
- [Yutu Setup Guide](references/setup.md) <br>
- [Super Chat Event List](references/superChatEvent-list.md) <br>
- [yutu project homepage](https://github.com/eat-pray-ai/yutu) <br>
- [yutu README](https://github.com/eat-pray-ai/yutu#readme) <br>
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include yutu command flags and OAuth configuration file names.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
