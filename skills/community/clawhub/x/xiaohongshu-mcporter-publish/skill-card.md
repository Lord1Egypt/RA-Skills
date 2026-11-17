## Description:

小红书创作者平台写帖子：mcporter 调用 chrome-devtools-mcp 操作浏览器，禁止 browser 工具。上传图片、填写标题正文，发布由用户手动完成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yewenwu1](https://clawhub.ai/user/yewenwu1)

### License/Terms of Use:


## Use Case:

External creators and operators use this skill to prepare Xiaohongshu image-and-text posts by opening the creator publish page, uploading user-specified Desktop images, and filling in title and body fields. The user reviews the prepared draft and completes publication manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent operates the Xiaohongshu creator page and could prepare unintended post content or select unintended images.

Mitigation: Review the completed draft in the browser before publishing; the skill explicitly leaves the publish action to the user.

Risk: The agent lists and uses files from the specific Desktop image folder named by the user.

Mitigation: Provide only the intended image folder and verify the selected images before manual publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yewenwu1/skills/xiaohongshu-mcporter-publish)
- [Xiaohongshu creator publish page](https://creator.xiaohongshu.com/publish/publish?source=official&from=tab_switch)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Text instructions with shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prepares a Xiaohongshu draft in the browser; final publication remains manual.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
