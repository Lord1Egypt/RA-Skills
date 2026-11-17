## Description:

Tavily Search lets agents use Tavily for web search, content extraction, site crawling, deep research, and API usage checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raydoomed](https://clawhub.ai/user/raydoomed)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to retrieve current web information, extract page content, crawl sites, produce research reports, and inspect Tavily API usage from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, URLs, crawl targets, and research prompts are sent to Tavily's external API.

Mitigation: Avoid sending secrets, private URLs, internal hostnames, or confidential research prompts to Tavily.

Risk: Site crawling can traverse external pages by default and consume API credits.

Mitigation: Use crawl limits plus domain and path filters before running broad crawl jobs.

## Reference(s):

- [Tavily API Reference](references/api-docs.md)
- [Tavily Website](https://tavily.com/)
- [Tavily Usage API Documentation](https://docs.tavily.com/documentation/api-reference/endpoint/usage)
- [ClawHub Skill Page](https://clawhub.ai/raydoomed/skills/tavilysearch)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON responses from Tavily-backed command-line workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY; requests may consume Tavily API credits.]

## Skill Version(s):

1.0.4 (source: server release evidence and SKILL.md version update)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
