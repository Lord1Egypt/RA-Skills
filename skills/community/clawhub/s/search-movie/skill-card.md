## Description:

一个基于 Model Context Protocol (MCP) 构建的智能电影和电视剧资源搜索工具，支持多源搜索和链接验证。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to search for movie or TV resources, inspect candidate titles and links, and validate whether selected playback pages are reachable. The skill requires a xiaobenyang.com API key before it can call the upstream service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a xiaobenyang.com API key and stores it in a local plaintext .env file.

Mitigation: Use a throwaway or restricted API key, keep .env private and out of version control, and rotate or remove the key after use.

Risk: Server security evidence reports stale mismatched gaokao and school-search references in the artifact.

Mitigation: Correct stale documentation and examples before broad distribution so users do not route requests to unrelated workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cainingnk/skills/search-movie)
- [XiaoBenYang API Key Provider](https://xiaobenyang.com)
- [XiaoBenYang MCP API Endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, API calls, guidance]

**Output Format:** [Markdown or plain text summarizing JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured XBY_APIKEY value; search results should be treated as unverified until validated by the URL validation tool.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
