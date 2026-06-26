## Description: <br>
Manage YouTube watermarks by helping agents set or unset watermarks for channel videos via the yutu CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate yutu CLI guidance for setting or removing a watermark on YouTube channel videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth credentials and a cached YouTube token. <br>
Mitigation: Keep client_secret.json and youtube.token.json out of source control and private storage, and revoke or delete the token when access is no longer needed. <br>
Risk: Running the generated set or unset commands can change channel branding. <br>
Mitigation: Verify the channel ID and watermark image before executing yutu watermark commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/OpenWaygate/youtube-watermark) <br>
- [Yutu Project Homepage](https://github.com/eat-pray-ai/yutu) <br>
- [Yutu Setup Guide](references/setup.md) <br>
- [Watermark Set Reference](references/watermark-set.md) <br>
- [Watermark Unset Reference](references/watermark-unset.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the yutu CLI plus YouTube OAuth credential and cached token configuration.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
