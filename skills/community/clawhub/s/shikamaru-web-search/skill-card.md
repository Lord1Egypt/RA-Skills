## Description:

Search the public web through Exa's hosted MCP endpoint without an API key for discovery tasks such as finding documentation, announcements, product pages, blog posts, comparisons, or current external context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shikamaru-cc](https://clawhub.ai/user/shikamaru-cc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover current public web sources before summarizing, comparing, or fetching detailed pages. It is intended for cases where the user needs relevant sources rather than direct retrieval from a known URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to Exa's hosted service.

Mitigation: Avoid secrets, private customer data, confidential internal project names, and other sensitive information in search queries.

Risk: Public web search context can be stale, incomplete, or conflicting.

Mitigation: Summarize the most relevant sources clearly, call out uncertainty or conflicts, and fetch authoritative pages when precise answers need verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shikamaru-cc/skills/shikamaru-web-search)
- [Exa MCP endpoint](https://mcp.exa.ai/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text search context, usually summarized by the agent in Markdown with source references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports query, result count, search depth, live crawl preference, and context length options.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
