## Description: <br>
Manage YouTube channel banners by guiding users through yutu CLI setup and banner upload commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure yutu OAuth credentials and upload a banner image to a specified YouTube channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth client secrets or cached YouTube tokens could be exposed if stored in shared repositories or logs. <br>
Mitigation: Keep client_secret.json and youtube.token.json out of shared repositories, restrict file access, add them to .gitignore, and revoke or rotate credentials if exposed. <br>
Risk: Running the upload command with the wrong channel ID or image can change a public YouTube channel banner. <br>
Mitigation: Confirm the channel ID and preview the banner image before executing yutu channelBanner insert. <br>
Risk: The skill depends on the external yutu CLI and YouTube OAuth configuration. <br>
Mitigation: Install yutu only from trusted sources and complete OAuth setup before using upload commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OpenWaygate/youtube-channel-banner) <br>
- [Channel Banner Insert](references/channelBanner-insert.md) <br>
- [Yutu Setup Guide](references/setup.md) <br>
- [yutu homepage](https://github.com/eat-pray-ai/yutu) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and command tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the yutu CLI, YouTube OAuth client credentials, a cached token, a channel ID, and a local banner image path.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
