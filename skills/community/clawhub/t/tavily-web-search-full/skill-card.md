## Description:

Complete Tavily toolkit for Search, Extract, Usage, Crawl, Map, and Research APIs with safety controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucetangc](https://clawhub.ai/user/brucetangc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to give agents Tavily-backed web search, URL extraction, usage reporting, site crawl/map, and research workflows. It is suited for RAG, research, and documentation lookup tasks that can safely send queries and URLs to Tavily.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tavily receives submitted queries, URLs, and research tasks.

Mitigation: Avoid sending confidential prompts or sensitive URLs unless the Tavily account and data handling posture are acceptable for the task.

Risk: The Tavily API key can be exposed through plaintext configuration or terminal output.

Mitigation: Prefer a protected environment variable, restrict local access to configuration files, and avoid printing real keys in logs or shell history.

Risk: Cached responses and logs may retain sensitive search or extraction content.

Mitigation: Use no-cache modes for confidential work and periodically review or clear local cache and log directories.

Risk: Crawl, map, and research operations can consume paid credits quickly.

Mitigation: Keep explicit enable and confirm flags in place, review limits before running broad jobs, and monitor usage with the included usage command.

Risk: Cron-based update checks introduce scheduled network activity and code changes.

Mitigation: Review the update workflow and destination before enabling scheduled checks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brucetangc/skills/tavily-web-search-full)
- [Tavily](https://tavily.com)
- [Tavily Documentation](https://docs.tavily.com)
- [Tavily Search API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/search)
- [Tavily Search Best Practices](https://docs.tavily.com/documentation/best-practices/best-practices-search)
- [Tavily Changelog](https://docs.tavily.com/changelog.md)
- [Tavily Rate Limits](https://docs.tavily.com/documentation/rate-limits.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, plain text, and Brave-compatible JSON depending on command flags.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY; API responses may be cached and logged locally; costlier crawl, map, and research operations require explicit enable or confirm flags.]

## Skill Version(s):

2.0.6 (source: server release evidence; artifact frontmatter lists 2.0.3 and README/release notes list 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
