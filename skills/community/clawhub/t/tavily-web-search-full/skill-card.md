## Description: <br>
Complete Tavily toolkit for Search, Extract, Usage, Crawl, Map, and Research APIs with safety controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BruceTangc](https://clawhub.ai/user/BruceTangc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill to run Tavily-powered web search, URL extraction, site mapping, site crawling, usage checks, and research workflows from agents or command-line scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches, URLs, and research prompts are sent to Tavily using a Tavily API key. <br>
Mitigation: Use the skill only for inputs appropriate to send to Tavily and manage TAVILY_API_KEY as a credential. <br>
Risk: Returned content and query data may be cached or logged locally under ~/.openclaw/. <br>
Mitigation: Use --no-cache where supported or clear ~/.openclaw/cache/tavily when working with sensitive material. <br>
Risk: Crawl, Map, and Research workflows can consume credits quickly. <br>
Mitigation: Use the documented --enable and --enable --confirm controls deliberately, check usage, and prefer lower-cost Search or Extract workflows when sufficient. <br>


## Reference(s): <br>
- [Tavily homepage](https://tavily.com) <br>
- [Tavily documentation](https://docs.tavily.com) <br>
- [Tavily Search API reference](https://docs.tavily.com/documentation/api-reference/endpoint/search) <br>
- [Tavily search best practices](https://docs.tavily.com/documentation/best-practices/best-practices-search) <br>
- [Tavily rate limits](https://docs.tavily.com/documentation/rate-limits.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, compact text, or JSON emitted by Python command-line scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAVILY_API_KEY; optional local caching and logs are written under ~/.openclaw/.] <br>

## Skill Version(s): <br>
2.0.6 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
