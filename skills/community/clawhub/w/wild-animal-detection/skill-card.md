## Description:

输入一张图像，输出图像中所有识别到的野生动物的检测框、置信度及标签。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to route image URLs or Base64-encoded image data to a wildlife detection service and return detected animal labels, confidence scores, and bounding boxes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in a local plaintext .env file.

Mitigation: Use a dedicated API key with limited quota, avoid committing or archiving the .env file, and rotate the key after use in shared workspaces.

Risk: Submitted images are sent to the external XiaoBenYang service for detection.

Mitigation: Avoid sending sensitive, regulated, or confidential images unless the external service is approved for that data.

Risk: Stale school-search references in the package make the documented scope less clear.

Mitigation: Review the skill files before deployment and confirm calls are limited to the wildlife detection tools expected for this release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/wild-animal-detection)
- [Publisher profile](https://clawhub.ai/user/cainingnk)
- [XiaoBenYang API key provider](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, guidance]

**Output Format:** [Markdown or structured JSON summary of API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns raw API response data with success and message fields; results depend on a configured XiaoBenYang API key and upstream service availability.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
