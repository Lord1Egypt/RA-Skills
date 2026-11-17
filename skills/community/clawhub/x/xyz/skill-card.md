## Description:

Xyz provides web search for agents across DuckDuckGo, Tavily, Bing, Google Custom Search, and SearXNG, returning structured result titles, links, and snippets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jwu26](https://clawhub.ai/user/jwu26)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agents use this skill to run current web searches, collect source titles, URLs, and snippets, and support market research, technical research, competitor analysis, literature review, and product research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to the selected external search provider.

Mitigation: Do not include secrets, private project names, customer data, regulated information, or other sensitive content in search queries.

Risk: The documentation references scripts/xyz.py, while the packaged executable script is scripts/web_search.py.

Mitigation: Use scripts/web_search.py until the package documentation is corrected.

Risk: Search results may be incomplete, unavailable, or misleading depending on network access and provider behavior.

Mitigation: Review returned sources and cross-check important claims before using the results in reports or decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jwu26/skills/xyz)
- [DuckDuckGo](https://duckduckgo.com)

## Skill Output:

**Output Type(s):** [text, JSON, markdown, shell commands, guidance]

**Output Format:** [Plain text or JSON search results; Markdown research reports may be produced by the documented workflow.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include query, count, titles, URLs, and snippets when returned by the selected provider.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
