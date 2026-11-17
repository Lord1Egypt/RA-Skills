## Description:

腾讯视频号发布。使用浏览器自动化技术，通过微信视频号助手发布视频作品。支持视频上传、标题、描述、话题标签、地理位置和原创声明。

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnyxu820](https://clawhub.ai/user/johnnyxu820)

### License/Terms of Use:


## Use Case:

External users use this skill to guide an agent through publishing a prepared MP4 video to Weixin Channels with title, description, topic tags, location, visibility, and originality declaration settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may publish to the wrong Weixin Channels account or with incorrect video metadata if the browser session or fields are not reviewed.

Mitigation: Before clicking publish, verify the logged-in account, video path, title, description, originality declaration, location, and visibility setting.

Risk: The publishing flow requires a logged-in Weixin account and user-selected local media, which can expose private content if the wrong file or visibility is chosen.

Mitigation: Use only intended video files and confirm whether the post is public or friends-only before final submission.

## Reference(s):

- [Weixin Channels Assistant](https://channels.weixin.qq.com)
- [Weixin Channels Create Post](https://channels.weixin.qq.com/platform/post/create)
- [Weixin Channels Content Management](https://channels.weixin.qq.com/platform/post/list)
- [ClawHub Skill Page](https://clawhub.ai/johnnyxu820/skills/weixin-video-publish)
- [Publisher Profile](https://clawhub.ai/user/johnnyxu820)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown instructions with structured publishing steps and example user prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-selected video file, OpenClaw browser access, and an authenticated Weixin Channels account.]

## Skill Version(s):

1.0.0 (source: artifact/_meta.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
