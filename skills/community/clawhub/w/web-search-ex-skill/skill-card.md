## Description:

A web search skill that lets agents run multi-engine searches across Baidu, Bing, and DuckDuckGo and crawl webpages without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yejinlei](https://clawhub.ai/user/yejinlei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve current web search results, crawl webpages, and return structured search data for downstream research, drafting, and automation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler can fetch arbitrary user-supplied HTTP or HTTPS URLs from the host environment.

Mitigation: Run the skill in a sandbox with outbound network rules that block localhost, private networks, cloud metadata endpoints, and sensitive internal services.

Risk: Search queries and crawl URLs may expose secrets, private URLs, or confidential topics to external search and crawling services.

Mitigation: Do not provide secrets, private URLs, or confidential queries to the skill; review inputs before execution in sensitive environments.

Risk: Dependencies are version-ranged rather than fully pinned.

Mitigation: Use pinned dependencies or a reviewed lockfile before production deployment.

## Reference(s):

- [Web Search skill page](https://clawhub.ai/yejinlei/skills/web-search-ex-skill)
- [yejinlei publisher profile](https://clawhub.ai/user/yejinlei)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [JSON object containing search results, snippets, URLs, status fields, and crawled page text or markdown when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result count is capped at 20; crawled text is truncated in the returned text field.]

## Skill Version(s):

1.3.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
