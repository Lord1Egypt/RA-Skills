## Description: <br>
Tavily search integration for agents, supporting web search, content extraction, real-time news lookup, site crawling, deep research, and usage checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guogithubname](https://clawhub.ai/user/guogithubname) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query Tavily for current web information, extract content from URLs, crawl scoped sites, generate research reports, and check Tavily account usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, URLs, crawl instructions, and research topics are sent to Tavily. <br>
Mitigation: Install only if sharing those inputs with Tavily is acceptable for the intended use case. <br>
Risk: The skill requires a Tavily API key and can consume account credits. <br>
Mitigation: Keep TAVILY_API_KEY private, monitor usage, and use result limits and lower-cost options where appropriate. <br>
Risk: Crawl and research operations can cover broad external content or run for longer than simple searches. <br>
Mitigation: Scope crawls with depth, breadth, limit, domain, and path filters; review research outputs before relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/guogithubname/tavilysearch-1-0-4) <br>
- [Tavily API complete documentation](references/api-docs.md) <br>
- [Tavily](https://tavily.com/) <br>
- [Tavily documentation](https://docs.tavily.com) <br>
- [Tavily Usage API reference](https://docs.tavily.com/documentation/api-reference/endpoint/usage) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, API Calls, Shell commands, Guidance] <br>
**Output Format:** [CLI-formatted text or JSON responses, with optional Markdown content from extraction, crawl, and research operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAVILY_API_KEY. Search, extract, crawl, research, get-research, and usage commands call Tavily APIs and may consume Tavily credits.] <br>

## Skill Version(s): <br>
1.0.4 (source: artifact _meta.json and SKILL.md changelog; ClawHub release metadata version 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
