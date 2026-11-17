## Description:

Tavilysearch integrates Tavily web search, content extraction, site crawling, research, and usage lookup for agents that need current web information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guogithubname](https://clawhub.ai/user/guogithubname)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search the web, retrieve current news or finance information, extract URL content, crawl sites, run Tavily research tasks, and check Tavily API usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, submitted URLs, crawl instructions, and research prompts are sent to Tavily.

Mitigation: Do not use the skill with secrets, private or internal URLs, regulated data, or proprietary research topics unless approved.

Risk: Site crawl mode can follow external domains by default.

Mitigation: Review crawl use before execution and constrain crawl scope with domain and path filters where appropriate.

Risk: The Tavily API key may be exposed if stored in shared source trees.

Mitigation: Store the key outside shared source trees where possible, and restrict its permissions and quota.

## Reference(s):

- [Tavily website](https://tavily.com/)
- [Tavily Search API](https://api.tavily.com/search)
- [Tavily usage endpoint documentation](https://docs.tavily.com/documentation/api-reference/endpoint/usage)
- [Bundled Tavily API reference](artifact/references/api-docs.md)
- [ClawHub release page](https://clawhub.ai/guogithubname/skills/tavilysearch-1-0-4)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Text, Markdown, and JSON returned from Tavily API-backed CLI commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY and sends submitted queries, URLs, crawl instructions, and research prompts to Tavily.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
