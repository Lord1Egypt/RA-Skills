## Description:

小红书自动发布技能 - 支持图片搜索下载、自动上传发布一键完成

This skill is ready for commercial/non-commercial use.

## Publisher:

[richardx0319](https://clawhub.ai/user/richardx0319)

### License/Terms of Use:

MIT-0

## Use Case:

Social media operators and content creators can use this skill to prepare Xiaohongshu note assets and guide a publishing workflow on macOS. The skill is intended for logged-in browser use where the user supplies or confirms the note topic, title, body, image, account, and final posting action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide public posting through a logged-in Xiaohongshu browser profile without clear final confirmation.

Mitigation: Confirm the target account and require explicit final approval or draft-only behavior before publishing.

Risk: Downloaded or selected images may be unsuitable for publication.

Mitigation: Inspect or replace the image before upload and ensure it is appropriate for the intended post.

Risk: Running the workflow with elevated privileges can increase the impact of local file or browser-profile mistakes.

Mitigation: Run the skill without elevated privileges and review it before installing or executing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richardx0319/skills/xiaohongshu-auto-publish-macos)
- [Xiaohongshu creator publishing page](https://creator.xiaohongshu.com/publish/publish)
- [Picsum image source](https://picsum.photos/800/1000)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with browser workflow steps, Python script execution instructions, and posting content text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepare an image file for upload and provide manual browser steps for completing publication.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
