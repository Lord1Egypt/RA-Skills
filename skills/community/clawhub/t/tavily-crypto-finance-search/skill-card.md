## Description:

Provides Tavily-backed web search and URL extraction for crypto, finance, market-news, and research workflows, with results formatted for agent use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mutamamo](https://clawhub.ai/user/mutamamo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to search Tavily for crypto, finance, Web3, market news, and selected reference content, or to extract full content from URLs for downstream summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, URLs, and extracted content are sent to Tavily as a third-party search provider.

Mitigation: Do not submit confidential queries, private URLs, signed links, or secrets unless sharing them with Tavily is acceptable.

Risk: The skill requires a Tavily API key for network search and extraction requests.

Mitigation: Provide TAVILY_API_KEY through the documented environment variable or local env file and avoid exposing the key in prompts, logs, or shared outputs.

Risk: Crypto and financial search results may be incomplete, stale, or unsuitable for trading or investment decisions.

Mitigation: Treat outputs as research inputs, verify important claims against authoritative sources, and avoid using search summaries as financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mutamamo/skills/tavily-crypto-finance-search)
- [Tavily website](https://tavily.com)
- [Tavily Search API endpoint](https://api.tavily.com/search)
- [Tavily Extract API endpoint](https://api.tavily.com/extract)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown, JSON, or brief plaintext search and extraction results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY; research mode can include a Tavily-generated answer summary; Markdown extraction output truncates displayed content to about 3000 characters per item.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
