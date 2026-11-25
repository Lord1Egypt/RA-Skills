## Description:

该MCP服务器使AI助手能够在Wikimedia Commons上搜索图片，提供详细的元数据和可选的缩略图组合，帮助AI模型进行视觉比较。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Wikimedia Commons for images, metadata, download URLs, and optional thumbnail composites for visual comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is advertised for Wikimedia image search but uses an unrelated XiaoBenYang API key and backend with unclear scope.

Mitigation: Review the skill before installing, only use it if you intend to trust XiaoBenYang with API keys and search parameters, and avoid sensitive queries.

Risk: The API key can be stored locally in plaintext in a .env file.

Mitigation: Use a temporary or restricted key, keep the .env file out of version control, and remove the local key entry when finished.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/wikimedia-search-images)
- [XiaoBenYang API key site](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration]

**Output Format:** [Markdown summaries with raw JSON result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Wikimedia image metadata, download URLs, and an optional thumbnail composite; requires an XBY_APIKEY.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
