## Description:

Crawl websites with Tavily and save extracted pages as local Markdown files or return structured crawl results for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evanydl](https://clawhub.ai/user/evanydl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to crawl documentation, knowledge bases, and website sections for offline analysis, context gathering, or local Markdown archives. It supports focused crawling through depth, breadth, path filters, semantic instructions, and chunked results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crawl targets and instructions are sent to Tavily.

Mitigation: Use only approved public URLs or authorized content, and avoid crawling private or internal sites unless approved.

Risk: The skill uses Tavily credentials from local auth or configuration files.

Mitigation: Prefer setting a scoped TAVILY_API_KEY for the command and keep credentials out of shared configuration when possible.

Risk: The OAuth flow may download and run an unpinned npm helper before first use.

Mitigation: Review or pin the mcp-remote helper and run first-time authentication in a controlled environment.

Risk: Broad crawl settings can collect more content than intended.

Mitigation: Start with conservative max_depth and limit values, and use select_paths, exclude_paths, or chunks_per_source to narrow results.

## Reference(s):

- [ClawHub Tavily Crawl Skill](https://clawhub.ai/evanydl/skills/tavily-crwal)
- [Tavily](https://tavily.com)
- [Tavily Crawl API Endpoint](https://api.tavily.com/crawl)
- [Tavily MCP Endpoint](https://mcp.tavily.com/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and JSON examples; runtime output is JSON or per-page Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write one Markdown file per crawled page when an output directory is provided.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
