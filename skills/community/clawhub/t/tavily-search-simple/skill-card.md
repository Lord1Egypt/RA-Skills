## Description:

使用 Tavily API 执行网络搜索，并以面向 LLM 和 AI Agent 的格式返回搜索结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhc888007](https://clawhub.ai/user/jhc888007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to run Tavily web searches from an agent workflow, with controls for search depth, topic, country, date filters, domains, images, and output format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, selected search options, and the Tavily API key are sent to Tavily for the intended search request.

Mitigation: Use only when this data sharing is acceptable, and avoid submitting sensitive queries or credentials beyond the required TAVILY_API_KEY.

Risk: The skill can read TAVILY_API_KEY from ~/.openclaw/.env if the environment variable is not set.

Mitigation: Keep ~/.openclaw/.env limited to intended OpenClaw secrets and review it before using the skill in shared or production environments.

Risk: Changing OpenClaw's default web search behavior can affect which search provider handles future searches.

Mitigation: Review the README guidance before disabling the default OpenClaw web search or routing searches to this skill.

## Reference(s):

- [Tavily Search API endpoint](https://api.tavily.com/search)
- [Tavily](https://www.tavily.com/)
- [Tavily Search API documentation](https://docs.tavily.com/documentation/api-reference/endpoint/search)
- [ClawHub skill page](https://clawhub.ai/jhc888007/skills/tavily-search-simple)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON, Brave-like JSON, or Markdown returned from a command-line search helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY and can include answer text, result snippets, URLs, raw content, and image URLs depending on options.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
