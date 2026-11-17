## Description:

Performs unified web search with Tavily as the primary engine and Zhipu web_search_prime as a fallback for current news, real-time information, and web lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mydearzsy](https://clawhub.ai/user/mydearzsy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when an agent needs recent web search results, news lookup, or online source discovery through a command-line search helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically use a locally stored generic API key for Zhipu, which is broader than the documentation clearly explains.

Mitigation: Review before installing, prefer dedicated TAVILY_API_KEY and ZHIPU_API_KEY values, and avoid relying on generic local credential lookup until it is removed or restricted.

Risk: Search queries may contain secrets, private customer data, or proprietary terms that are sent to Tavily or Zhipu.

Mitigation: Do not submit sensitive data as search queries unless the user is comfortable sending it to the selected provider.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mydearzsy/skills/tavily-zhipu-search)
- [Tavily Search API endpoint](https://api.tavily.com/search)
- [Zhipu web_search_prime MCP endpoint](https://open.bigmodel.cn/api/mcp/web_search_prime/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-formatted search results and command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tavily or Zhipu API credentials; search queries are sent to the selected external search provider.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
