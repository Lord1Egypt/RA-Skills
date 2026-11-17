## Description:

Tavily Search Optimized lets an agent run Tavily web searches, return concise results, and optionally include answer summaries with caching and configurable output formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[confidentkai](https://clawhub.ai/user/confidentkai)

### License/Terms of Use:

MIT-0

## Use Case:

Agents, developers, and external users use this skill when they need web search, source lookup, links, or concise search-result summaries through Tavily when Brave web_search is unavailable or undesired.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verbose output can expose the Tavily API key through request or troubleshooting details.

Mitigation: Avoid verbose mode unless output is controlled, and redact credentials from logs or shared transcripts.

Risk: A configured Tavily cache directory can be recursively deleted by cache-clearing behavior.

Mitigation: Use a dedicated cache directory and verify TAVILY_CACHE_DIR before clearing cached results.

Risk: Search queries are sent to Tavily and query/results data can be stored locally in cache files.

Mitigation: Do not submit sensitive queries unless approved for Tavily use, and manage cache TTL, location, and retention according to local policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/confidentkai/skills/tavily-search-optimized-v1)
- [Tavily](https://tavily.com)
- [Tavily Search API endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON, Markdown, or plain text search results with command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include Tavily answer summaries; returns up to 10 search results; cache TTL and cache directory are configurable.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; bundled artifact frontmatter and changelog report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
