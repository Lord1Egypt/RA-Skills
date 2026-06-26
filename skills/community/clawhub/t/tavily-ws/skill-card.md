## Description: <br>
Connect agents to the web using Tavily APIs and SDKs for search, URL extraction, semantic crawls, site mapping, and asynchronous deep research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to integrate Tavily web search, extraction, crawl, map, and research APIs into RAG and research workflows. It provides reference guidance, API parameters, troubleshooting steps, and Python request patterns for using Tavily efficiently. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tavily queries, target URLs, and extracted or crawled page content are shared with an external API provider. <br>
Mitigation: Avoid submitting sensitive data or unauthorized targets, and review data-handling requirements before using search, extraction, crawl, map, or research workflows. <br>
Risk: The skill requires a sensitive Tavily API credential. <br>
Mitigation: Store the API key in a secret manager or environment variable, avoid hard-coding it in prompts or files, and rotate it if exposed. <br>
Risk: Crawl and deep research workflows can consume quota and may hit rate limits. <br>
Mitigation: Monitor usage, respect Tavily rate limits, and use retry/backoff handling for 429 and transient server errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simonpierreboucher02/tavily-ws) <br>
- [Core Search & Extraction Workflows](references/workflows.md) <br>
- [Tavily API Reference & Technical Specifications](references/api_reference.md) <br>
- [Troubleshooting & Diagnostics Runbook](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with Python code examples and API parameter tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Tavily API key and sends queries, URLs, and extracted or crawled page content to Tavily.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
