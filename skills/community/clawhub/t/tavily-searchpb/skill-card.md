## Description: <br>
Web search, extraction, crawling, mapping, and deep research via Tavily API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[popxool868-abcd](https://clawhub.ai/user/popxool868-abcd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily-powered web search, URL extraction, website crawling, site mapping, and deep research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search, crawl, extraction, and research requests are sent to Tavily for processing. <br>
Mitigation: Avoid sending confidential queries, private URLs, internal endpoints, or personal data unless authorized to share them with Tavily. <br>
Risk: The skill requires a Tavily API key. <br>
Mitigation: Treat TAVILY_API_KEY as a secret and provide it through environment variables or a secret manager. <br>


## Reference(s): <br>
- [Tavily API documentation](https://docs.tavily.com) <br>
- [Tavily](https://tavily.com) <br>
- [openclaw-tavily npm package](https://www.npmjs.com/package/openclaw-tavily) <br>
- [Tavily Search on ClawHub](https://clawhub.ai/popxool868-abcd/tavily-searchpb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with answers, source lists, extracted content, URL maps, research reports, and inline bash examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAVILY_API_KEY; search results are capped by requested result count, and some crawl or source snippets may be truncated.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence, released 2026-03-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
