## Description: <br>
帮助用户在抖音、快手、B站、小红书和微信视频号发布视频和图文内容，并要求用户在本地浏览器中确认登录和发布操作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hitjcl](https://clawhub.ai/user/hitjcl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and social media operators use this skill to prepare platform-specific publishing guidance and browser-assisted posting steps for video or image-text content. It is intended for accounts already logged in locally by the user, with user confirmation before final publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing from a logged-in social account can post to the wrong account or publish unintended content. <br>
Mitigation: Confirm the exact platform, account, file, title, description, tags, and final publish action before proceeding; test with a non-primary account when practical. <br>
Risk: Browser-assisted workflows depend on active local sessions and visible page state. <br>
Mitigation: Manually log in through the browser, do not provide credentials to the agent, and stop if the account or page context is unexpected. <br>
Risk: Each platform has its own file-size, duration, aspect-ratio, and content rules. <br>
Mitigation: Review the generated platform guidance and the platform's own publishing requirements before uploading or posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hitjcl/social-video-publish) <br>
- [Douyin creator upload](https://creator.douyin.com/creator/micro/upload) <br>
- [Kuaishou creator profile](https://cp.kuaishou.com/profile) <br>
- [Bilibili creator publishing](https://member.bilibili.com/v/publish/spaces) <br>
- [Xiaohongshu creator publishing](https://creator.xiaohongshu.com/creator/post/create) <br>
- [WeChat Channels login](https://channels.weixin.qq.com/login) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with optional shell command output and browser command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include platform-specific publishing URLs, validation messages, recommended tags, and user-confirmed browser workflow steps.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
