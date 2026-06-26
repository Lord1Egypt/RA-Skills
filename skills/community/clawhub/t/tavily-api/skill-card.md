## Description: <br>
Tavily API integration with managed API key authentication for AI-powered web search, content extraction from URLs, website crawling, site structure mapping, and research tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to call Tavily through Maton for web search, URL content extraction, crawling, site mapping, and research workflows with citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches, URLs, crawl targets, extracted content, and research prompts are sent through Maton and Tavily. <br>
Mitigation: Use the skill only for information intended for those external services, and avoid secrets, confidential internal URLs, regulated data, or sensitive research targets unless that sharing is approved. <br>
Risk: Connection management commands can create, select, list, or delete Tavily API key connections. <br>
Mitigation: List and confirm the intended connection before selecting or deleting it, especially when multiple active Tavily connections exist. <br>
Risk: The skill requires a MATON_API_KEY credential for authenticated gateway access. <br>
Mitigation: Store MATON_API_KEY in the execution environment and avoid hard-coding or logging the key in prompts, scripts, or shared outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/tavily-api) <br>
- [Maton](https://maton.ai) <br>
- [Tavily API Documentation](https://docs.tavily.com) <br>
- [Tavily Search API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/search) <br>
- [Tavily Extract API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/extract) <br>
- [Tavily Crawl API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/crawl) <br>
- [Tavily Research API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/research) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline JSON, Python, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY for authenticated Maton gateway calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
