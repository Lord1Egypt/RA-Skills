## Description:

Use Tavily web search/discovery to find URLs/sources, do lead research, gather up-to-date links, or produce a cited summary from web results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tylordius](https://clawhub.ai/user/tylordius)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run Tavily searches from the terminal, collect current source URLs, and gather search-result JSON for research or citation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and the Tavily API key are sent to Tavily's API.

Mitigation: Avoid sensitive private data in search queries and scope TAVILY_API_KEY to this use where the environment supports it.

Risk: The CLI supports only a subset of Tavily request fields.

Mitigation: Use the documented parameters for discovery workflows or call Tavily directly when unsupported API fields are required.

## Reference(s):

- [Tavily API notes](references/tavily-api.md)
- [Tavily search endpoint](https://api.tavily.com/search)
- [ClawHub skill page](https://clawhub.ai/tylordius/skills/tavily-tool)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON search responses or newline-delimited URLs, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY; supports query, max_results, include_domains, and exclude_domains.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
