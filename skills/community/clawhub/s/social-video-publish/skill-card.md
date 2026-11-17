## Description:

Helps agents guide or automate user-approved publishing of video and image-text content to Douyin, Kuaishou, Bilibili, Xiaohongshu, and WeChat Channels using the user's already logged-in local browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hitjcl](https://clawhub.ai/user/hitjcl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to prepare and publish video or image-text posts across supported Chinese social platforms while keeping login and final publishing actions under user control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser guidance or automation may act in social accounts that are already logged in.

Mitigation: Confirm the target platform, account, video file, title, description, tags, and final publish action before proceeding.

Risk: Posting from a primary account can have account, reputation, or policy consequences if content or platform settings are wrong.

Mitigation: Test with a non-primary account first, review each platform's posting rules, and monitor account activity after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hitjcl/skills/social-video-publish)
- [ClawHub source page](https://clawhub.ai/hitjcl/social-publish)
- [Douyin creator upload](https://creator.douyin.com/creator/micro/upload)
- [Kuaishou creator profile](https://cp.kuaishou.com/profile)
- [Bilibili creator upload](https://member.bilibili.com/v/publish/spaces)
- [Xiaohongshu creator post](https://creator.xiaohongshu.com/creator/post/create)
- [WeChat Channels login](https://channels.weixin.qq.com/login)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown-style guidance with generated browser-command text and command-line script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-confirmed browser actions and existing platform login; evidence states it does not store credentials.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
