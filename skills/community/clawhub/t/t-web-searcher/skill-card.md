## Description:

AI-optimized web search via Tavily API. Returns concise, relevant results for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hhjack](https://clawhub.ai/user/hhjack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to run Tavily-backed web searches and extract page content from URLs for concise source material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The search script lets Tavily response metadata choose formatter code to import and run.

Mitigation: Review before installing and restrict formatter selection to a local allowlist before deployment.

Risk: Search queries, requested URLs, and the Tavily API key are sent to Tavily.

Mitigation: Use a scoped API key and avoid sending sensitive queries or private URLs unless Tavily use is approved.

## Reference(s):

- [Tavily](https://tavily-search.com)
- [Tavily Search API endpoint](https://api.tavily-search.com/search)
- [Tavily Extract API endpoint](https://api.tavily-search.com/extract)
- [ClawHub skill page](https://clawhub.ai/hhjack/skills/t-web-searcher)
- [ClawHub publisher profile](https://clawhub.ai/user/hhjack)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style terminal output with search answers, source lists, snippets, extracted page text, and failed URL notices.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and TAVILY_API_KEY; supports result count, deep search, general/news topics, and news recency filtering.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
