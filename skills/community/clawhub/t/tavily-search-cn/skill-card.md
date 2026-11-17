## Description:

Tavily AI 搜索工具，专为AI Agent设计的联网搜索能力，支持实时搜索、深度研究、图片搜索、引用生成，返回结构化搜索结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add Tavily-powered web search, research-style result gathering, image search, citations, and structured search output to an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release stores and ships a Tavily API key in plaintext.

Mitigation: Remove the bundled key, rotate it, avoid committing config.json, and use an environment variable or private secret store for future keys.

Risk: Search queries are sent to Tavily when the tool is used.

Mitigation: Review queries before use and avoid sending secrets, personal data, or confidential business information unless the deployment has approved Tavily for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/tavily-search-cn)
- [Publisher profile](https://clawhub.ai/user/paudyyin)
- [Tavily website](https://tavily.com/)
- [Tavily Search API endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, API Calls, Shell commands, Configuration]

**Output Format:** [CLI text output or JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include answer text, result titles, source URLs, publication dates, summaries, image URLs, and response time.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
