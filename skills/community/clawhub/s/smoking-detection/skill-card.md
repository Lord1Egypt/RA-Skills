## Description:

输入一张图像，对其中的香烟目标进行检测，输出图片中所有目标的检测框、置信度和标签。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit an image by URL or base64 data and receive detected cigarette objects with bounding boxes, confidence scores, and labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys are stored in plaintext .env files.

Mitigation: Use only a rotatable API key, keep the workspace private, and avoid committing, backing up, or sharing .env files.

Risk: Images and API keys are sent to a remote Xiaobenyang service.

Mitigation: Use only non-sensitive images and confirm the remote service is acceptable before installation or execution.

Risk: The upstream API endpoint is configurable.

Mitigation: Validate or pin the intended API host before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/smoking-detection)
- [Xiaobenyang API key portal](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, json, api calls, configuration guidance]

**Output Format:** [Markdown summary of JSON detection results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an API key and either an image URL or base64-encoded image input.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
