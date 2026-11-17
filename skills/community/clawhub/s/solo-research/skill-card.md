## Description:

Deep market research for competitor analysis, user pain points, SEO/ASO keywords, naming and domain availability, and TAM/SAM/SOM sizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fortunto2](https://clawhub.ai/user/fortunto2)

### License/Terms of Use:

MIT

## Use Case:

Developers, founders, and product teams use this skill to research a product idea before PRD generation, including competitors, pain points, search keywords, naming options, domains, and market sizing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search prior sessions and sibling project source data, which may expose confidential context or cross-project information.

Mitigation: Use the skill only where cross-project research is acceptable, or disable session_search and codegraph/project_code_search tools unless the user explicitly wants that data consulted.

Risk: The skill performs public web and Reddit research that may include unreliable, stale, or incomplete market signals.

Mitigation: Review generated findings and source links before using the report for product, market, or investment decisions.

## Reference(s):

- [Domain & Naming Check Reference](references/domain-check.md)
- [research.md Output Template](references/research-template.md)
- [PRAW Python Reddit API Wrapper](https://github.com/praw-dev/praw)
- [SearXNG Docker Tavily Adapter](https://github.com/fortunto2/searxng-docker-tavily-adapter)
- [PullPush Reddit Submission Search](https://api.pullpush.io/reddit/submission/search)
- [TrustMRR Scraper](https://apify.com/actor_builder/trustmrr-scraper/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables, source links, summary bullets, recommendation, and generated docs/research.md file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use public web, Reddit, YouTube, Product Hunt, market reports, domain lookup commands, and optional MCP search tools when available.]

## Skill Version(s):

1.7.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
