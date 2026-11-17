## Description:

高精度文字识别。输入包含文本的图像，自动检测并识别内容。适用于各类文档、广告牌、屏幕截图等场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xby-skill](https://clawhub.ai/user/xby-skill)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send document, sign, screenshot, or other image inputs to the Xiaobenyang OCR API and receive recognized text results for presentation to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OCR inputs and image contents are sent to a third-party API provider.

Mitigation: Use only when the user is comfortable sharing the image with Xiaobenyang, and avoid highly sensitive documents unless the provider's data handling is understood.

Risk: The skill can store the Xiaobenyang API key in a local plaintext .env file.

Mitigation: Protect or remove the .env file when access is no longer needed, and rotate the API key if it may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xby-skill/skills/xby-ocr-pro)
- [Xiaobenyang API key provider](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Guidance]

**Output Format:** [Markdown summary of OCR API results with raw JSON available from tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value and accepts either an image URL or base64-encoded image data.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
