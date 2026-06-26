## Description: <br>
Build production-ready Tavily integrations with best practices baked in. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evanYDL](https://clawhub.ai/user/evanYDL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement Tavily-powered web search, extraction, crawling, URL discovery, and research workflows in agents, RAG systems, and application integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example Tavily workflows may send queries, URLs, or extracted content to external services. <br>
Mitigation: Do not send secrets, internal-only URLs, personal data, or regulated content unless the organization has approved that data flow. <br>
Risk: Database-persistence examples can retain retrieved content or metadata beyond the immediate agent run. <br>
Mitigation: Review storage behavior, retention policy, and access controls before enabling persistence in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evanYDL/tavily-bestpractices) <br>
- [SDK Reference](references/sdk.md) <br>
- [Search API Reference](references/search.md) <br>
- [Extract API Reference](references/extract.md) <br>
- [Crawl and Map API Reference](references/crawl.md) <br>
- [Research API Reference](references/research.md) <br>
- [Framework Integrations](references/integrations.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline Python, JavaScript, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; examples may call Tavily and related integration services when a user implements them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
