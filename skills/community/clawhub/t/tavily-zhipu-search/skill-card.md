## Description: <br>
Provides unified web search for current news, real-time information, and web lookup, using Tavily first and falling back to Zhipu web_search_prime when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mydearzsy](https://clawhub.ai/user/mydearzsy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to answer requests that require recent news, real-time information, or web research by running a Tavily search with Zhipu fallback when Tavily is unavailable or fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Zhipu fallback can reuse a provider API key from ~/.openclaw/openclaw.json when ZHIPU_API_KEY is not set. <br>
Mitigation: Set explicit TAVILY_API_KEY and ZHIPU_API_KEY values, or remove the openclaw.json fallback if local provider credentials should not be reused. <br>
Risk: Search queries are sent to external Tavily or Zhipu services and may include sensitive terms. <br>
Mitigation: Avoid private, regulated, or confidential search terms unless the configured provider and account are approved for that data. <br>
Risk: If neither provider key is configured, the skill returns an error instead of search results. <br>
Mitigation: Configure at least one provider key before relying on the skill in an agent workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mydearzsy/tavily-zhipu-search) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>
- [Zhipu web_search_prime MCP endpoint](https://open.bigmodel.cn/api/mcp/web_search_prime/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown-formatted search results with titles, excerpts, URLs, summaries, and error messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAVILY_API_KEY or ZHIPU_API_KEY; Tavily recency is controlled with --days and constrained to 1-7 days.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
