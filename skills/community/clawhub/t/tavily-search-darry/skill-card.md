## Description:

Tavily Search integrates Tavily web search, news, crawl, extract, and research capabilities for agents that need current web results, content extraction, and cited research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darryek](https://clawhub.ai/user/darryek)

### License/Terms of Use:


## Use Case:

Developers and external agent users use this skill to search the web, gather current news, extract page content, crawl websites into markdown, and produce cited research using Tavily.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts may read Tavily OAuth tokens from a shared local MCP token cache when TAVILY_API_KEY is unset.

Mitigation: Set TAVILY_API_KEY explicitly in a scoped environment and review token access before running the skill.

Risk: The OAuth fallback may run an unpinned npm helper through npx.

Mitigation: Avoid the OAuth fallback unless unpinned package execution is acceptable; prefer an explicit Tavily API key.

Risk: Queries, URLs, and retrieved page content may be sent to Tavily for search, extraction, crawl, or research operations.

Mitigation: Do not use the skill with confidential URLs or regulated content unless Tavily processing is approved.

## Reference(s):

- [Tavily](https://tavily.com)
- [SDK Reference](tavily-best-practices/references/sdk.md)
- [Search API Reference](tavily-best-practices/references/search.md)
- [Extract API Reference](tavily-best-practices/references/extract.md)
- [Crawl and Map API Reference](tavily-best-practices/references/crawl.md)
- [Research API Reference](tavily-best-practices/references/research.md)
- [Integrations Reference](tavily-best-practices/references/integrations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, text, and optional local markdown files from shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash and Tavily authentication through TAVILY_API_KEY or OAuth.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
