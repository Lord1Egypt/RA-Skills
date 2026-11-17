## Description:

腾讯视频号发布 uses browser automation to guide publishing a video to WeChat Channels when the user asks to post to 视频号.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnyxu820](https://clawhub.ai/user/johnnyxu820)

### License/Terms of Use:


## Use Case:

Developers, operators, and content publishing agents use this skill to publish prepared videos to WeChat Channels through a browser workflow with QR-code login, upload, title, description, visibility, location, originality declaration, and post-publication checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate in a live WeChat Channels account and publish visible content.

Mitigation: Use a dedicated publishing account where practical and require the user to review title, description, visibility, location, and originality settings before clicking publish.

Risk: Server security evidence says the skill adds preset public wording, hashtags, a fixed Suzhou Center location, and an originality declaration without clear user approval.

Mitigation: Treat these fields as proposed defaults only; confirm or edit the wording, tags, location, and originality declaration with the user before publication.

Risk: Duplicate publishing can occur if success is not checked before retrying.

Mitigation: Check the WeChat Channels content management page or refresh confirmation before attempting another publish action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnyxu820/skills/wechat-video-publish)
- [WeChat Channels publish page](https://channels.weixin.qq.com/platform/post/create)

## Skill Output:

**Output Type(s):** [Guidance, Browser automation actions, Text]

**Output Format:** [Markdown-style workflow guidance with browser actions and publication field text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local video file, WeChat QR-code login, Browser Relay/OpenClaw Chrome profile access, and manual review before publishing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
