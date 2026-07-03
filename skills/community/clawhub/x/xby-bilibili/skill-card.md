## Description: <br>
用于哔哩哔哩API的MCP服务器，支持视频搜索、用户内容获取等多种操作，适用于哔哩哔哩内容管理和数据分析场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alinklab](https://clawhub.ai/user/alinklab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content analysts use this skill to search Bilibili users and videos, retrieve user posts, collections, and danmaku, and summarize API results for content management or data analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a third-party Xiaobenyang API key and may save it to a local .env file in plaintext. <br>
Mitigation: Prefer setting XBY_APIKEY through the environment, avoid sharing unnecessary credentials, and remove any saved .env key after use. <br>
Risk: Bilibili-related queries and requested content identifiers are sent to Xiaobenyang's API service. <br>
Mitigation: Use the skill only when you trust the third-party service and avoid submitting sensitive or private query content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alinklab/skills/xby-bilibili) <br>
- [Xiaobenyang API key site](https://xiaobenyang.com) <br>
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, JSON, guidance, configuration] <br>
**Output Format:** [JSON API responses summarized as text or Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY_APIKEY for Xiaobenyang API access; upstream results are returned in the raw field before the agent summarizes them.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
