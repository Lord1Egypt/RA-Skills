## Description:

使用浏览器自动化在网页版小红书创作者服务平台发布视频笔记。

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnyxu820](https://clawhub.ai/user/johnnyxu820)

### License/Terms of Use:


## Use Case:

Creators and agents use this skill to publish video notes to a logged-in Xiaohongshu creator account, including upload, title and body entry, cover setup, location selection, and post-publish verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates publishing to a live Xiaohongshu creator account.

Mitigation: Require final confirmation of the account, video, cover, title, body, location, and intent to publish before clicking the publish button.

Risk: The skill includes a fixed location value of 苏州中心.

Mitigation: Remove or override the location unless it is accurate for the post.

Risk: A repeated run could publish duplicate content.

Mitigation: Check local logs and the platform content management page before retrying, and stop after a successful publish confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnyxu820/skills/xiaohongshu-video-publish)
- [Xiaohongshu creator video publish page](https://creator.xiaohongshu.com/publish/publish?source=official&from=tab_switch&target=video)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw Chrome extension access and a logged-in Xiaohongshu creator account.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
