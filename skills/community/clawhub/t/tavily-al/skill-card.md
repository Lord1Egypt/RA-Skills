## Description: <br>
Instructional agent skill that teaches an AI agent when and how to use Tavily for live web search, content extraction, crawling, site mapping, source evaluation, citation discipline, error handling, cost control, freshness, and prompt-injection safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to teach agents how to perform live web research through Tavily, choose the appropriate search or retrieval operation, and produce cited, verifiable answers. It is intended for agents that already have Tavily tools or an approved HTTP client available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Tavily credentials. <br>
Mitigation: Configure TAVILY_API_KEY through the host environment, never paste keys into prompts, and do not print or log key material. <br>
Risk: Web search and extraction may expose confidential, regulated, or internal information to an external service. <br>
Mitigation: Avoid sending secrets, confidential topics, internal URLs, private documents, or regulated data to Tavily unless the organization has approved that data flow. <br>
Risk: Retrieved web content can contain inaccurate information or prompt-injection attempts. <br>
Mitigation: Treat retrieved content as untrusted data, prefer authoritative sources, cross-check important claims, and cite the actual source URLs used. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simonpierreboucher02/tavily-al) <br>
- [Tavily official documentation](https://docs.tavily.com) <br>
- [Endpoint reference](reference/endpoints.md) <br>
- [Parameter reference](reference/parameters.md) <br>
- [Response field reference](reference/response-fields.md) <br>
- [Common error handling](reference/common-errors.md) <br>
- [Safety and security reference](reference/safety-and-security.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown guidance with inline examples, checklists, and citation patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a host-provided TAVILY_API_KEY and Tavily-compatible search, extract, crawl, or map tools for live retrieval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
