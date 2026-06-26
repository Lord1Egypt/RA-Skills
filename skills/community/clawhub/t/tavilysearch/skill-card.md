## Description: <br>
Tavily Search helps agents run web searches, extract page content, crawl sites, create research reports, and check Tavily usage through the Tavily API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raydoomed](https://clawhub.ai/user/raydoomed) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to give agents Tavily-backed live web search, URL extraction, website crawling, research-report generation, and usage lookup capabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, URLs, crawl targets, and research prompts are sent to Tavily. <br>
Mitigation: Use the skill only for data you are comfortable sending to Tavily, and avoid submitting secrets or internal-only URLs. <br>
Risk: Broad crawls or deep research requests can consume Tavily credits quickly. <br>
Mitigation: Use domain and path filters, conservative crawl limits, and usage checks to monitor credit consumption. <br>
Risk: The skill requires a Tavily API key. <br>
Mitigation: Keep TAVILY_API_KEY private and store it only in the intended local configuration. <br>


## Reference(s): <br>
- [ClawHub Tavily Search Skill Page](https://clawhub.ai/raydoomed/tavilysearch) <br>
- [Tavily Website](https://tavily.com/) <br>
- [Tavily API Documentation](references/api-docs.md) <br>
- [Tavily Usage Endpoint](https://docs.tavily.com/documentation/api-reference/endpoint/usage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text, Markdown, or JSON returned from Tavily API-backed commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include search result snippets, extracted page content, crawl summaries, research reports with citations, usage metrics, and Tavily credit usage when requested.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and SKILL.md version history, released 2026-03-15) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
