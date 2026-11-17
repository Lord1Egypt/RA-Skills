## Description:

小红书长文发布。用于在网页版小红书创作服务平台发布长文笔记。

This skill is ready for commercial/non-commercial use.

## Publisher:

[enjoytdl](https://clawhub.ai/user/enjoytdl)

### License/Terms of Use:


## Use Case:

External users use this skill when they want an agent to publish a long-form Xiaohongshu note through the web creator platform. It guides browser-based drafting, formatting, template selection, and publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content to a real Xiaohongshu account.

Mitigation: Require explicit final user confirmation before clicking the publish button.

Risk: The invocation trigger is broad and may match casual requests to write or post Xiaohongshu content.

Mitigation: Invoke only when the user clearly intends to publish to Xiaohongshu, and confirm the target account and post content before publishing.

Risk: The Xiaohongshu web interface may change after release.

Mitigation: Review the page state during execution and stop for user guidance if the browser workflow no longer matches the visible interface.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/enjoytdl/skills/xiaohongshu-publish)
- [Xiaohongshu creator publish page](https://creator.xiaohongshu.com/publish/publish?source=official)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown instructions for a browser-based publishing workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in a real public account action when the publishing workflow is completed.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
