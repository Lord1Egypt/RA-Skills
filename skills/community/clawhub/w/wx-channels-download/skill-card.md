## Description: <br>
Resolve and download WeChat Channels / 微信视频号 share links directly, using the online sph resolver and curl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imchao9](https://clawhub.ai/user/imchao9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to resolve WeChat Channels share links through a documented online resolver and download permitted videos without installing a local proxy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Share-link metadata is sent to the documented online resolver service. <br>
Mitigation: Use the skill only when the user is comfortable sending the WeChat share link to that resolver. <br>
Risk: The skill downloads media to the user's Downloads folder and can overwrite an existing file if the same filename is reused. <br>
Mitigation: Choose a unique filename when preserving an existing download matters. <br>
Risk: The skill can be misused to download content the user is not allowed to access or save. <br>
Mitigation: Use it only for content the user has permission to access and download, and do not use it to bypass platform restrictions. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/imchao9/wx-channels-download) <br>
- [Upstream wx_channels_download Repository](https://github.com/ltaoo/wx_channels_download) <br>
- [Share Link Download Commands](references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads media to ~/Downloads; filename can be provided or derived from resolver metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
