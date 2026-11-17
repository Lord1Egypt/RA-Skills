## Description:

Connect agents to the web using Tavily APIs and SDKs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect agents to Tavily web search, extraction, crawl, map, and asynchronous research APIs. It supports RAG workflows, targeted web extraction, site mapping, and resilient API-call patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send search queries, target URLs, and extracted web-research context to Tavily.

Mitigation: Use it only where Tavily's data-handling terms are appropriate, and avoid sending private or sensitive internal URLs.

Risk: The skill depends on a Tavily API key for web-search and extraction workflows.

Mitigation: Store the API key in environment variables or the host platform's secret manager rather than embedding it in prompts or files.

Risk: High-volume API use can hit Tavily rate limits.

Mitigation: Use the provided retry and backoff guidance, including respect for the retry-after header on 429 responses.

## Reference(s):

- [Tavily API Reference & Technical Specifications](references/api_reference.md)
- [Core Search & Extraction Workflows](references/workflows.md)
- [Troubleshooting & Diagnostics Runbook](references/troubleshooting.md)
- [ClawHub skill page](https://clawhub.ai/simonpierreboucher02/skills/tavily-ws)
- [Publisher profile](https://clawhub.ai/user/simonpierreboucher02)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python code examples and API parameter references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Tavily API requests that send search queries, target URLs, and extracted web-research context to Tavily.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
