## Description: <br>
Automatically selects and runs a search, crawl, or browsing tool based on a query or URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sean810720](https://clawhub.ai/user/sean810720) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route web research tasks to tools such as jina.ai, DuckDuckGo, Firecrawl, Tavily, Brave Search, or agent-reach. It is intended for reading pages, searching across sources, crawling sites, and returning concise terminal or JSON results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, URLs, or crawled content may be sent to external search, crawling, or browsing providers. <br>
Mitigation: Avoid confidential queries, private URLs, and account-backed searches unless the selected provider is trusted; use --engine when predictable routing is required. <br>
Risk: Optional providers require API keys or OAuth-backed tools that may expose account or quota risk if misconfigured. <br>
Mitigation: Keep API keys out of version control and review separately installed tools such as firecrawl, tavily-search, and agent-reach before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sean810720/search-strategy-skill) <br>
- [OpenClaw homepage](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text or JSON, with Markdown content returned by supported readers and crawlers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes requests by query, URL, engine override, crawl mode, verbosity, and maximum result count.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
