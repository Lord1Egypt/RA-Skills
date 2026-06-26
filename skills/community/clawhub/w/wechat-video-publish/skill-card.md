## Description: <br>
Automates publishing a local video to WeChat Channels through a browser session, including upload, title and description entry, visibility selection, and final publish checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnyxu820](https://clawhub.ai/user/Johnnyxu820) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to guide an agent through posting prepared video content to a logged-in WeChat Channels account. It is intended for browser-assisted publishing workflows where the user can confirm the final content and publish action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish from a logged-in WeChat Channels account. <br>
Mitigation: Require explicit user confirmation of the final video, title, description, hashtags, visibility, and publish action before posting. <br>
Risk: The skill adds fixed public text, location, and originality claims that may not match the user's intent. <br>
Mitigation: Remove or confirm the fixed appended phrase, fixed location, and originality declaration for each post. <br>


## Reference(s): <br>
- [WeChat Channels post creation page](https://channels.weixin.qq.com/platform/post/create) <br>
- [ClawHub skill page](https://clawhub.ai/Johnnyxu820/wechat-video-publish) <br>
- [Publisher profile](https://clawhub.ai/user/Johnnyxu820) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown instructions for browser automation steps and user confirmations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a browser session, OpenClaw Chrome extension, a local video file, and WeChat QR-code login.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
