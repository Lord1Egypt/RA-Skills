## Description:

Instructional agent skill that teaches an AI agent when and how to use Tavily for live web search, content extraction, crawling, and site mapping, including operation selection, query planning, source evaluation, citation discipline, error handling, cost control, freshness, and security against prompt injection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to teach agents how to decide when live web retrieval is needed, select the right Tavily operation, evaluate sources, cite claims, and handle search or extraction failures safely.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and requested URLs are sent to Tavily for live retrieval.

Mitigation: Install only when live web retrieval is intended, and avoid sending secrets or private local data in queries or URLs.

Risk: The Tavily API key could be exposed if handled directly by the agent.

Mitigation: Keep TAVILY_API_KEY in the host environment and prefer MCP or tool-based use so the raw key is not surfaced to the agent.

Risk: Retrieved web pages can contain misleading content or prompt-injection instructions.

Mitigation: Treat retrieved content only as untrusted source data, ignore embedded instructions, cross-check important claims, and cite the actual source URLs used.

## Reference(s):

- [Tavily Official Documentation](https://docs.tavily.com)
- [ClawHub Skill Page](https://clawhub.ai/simonpierreboucher02/skills/tavily-al)
- [README](artifact/README.md)
- [Tavily Endpoints Reference](artifact/reference/endpoints.md)
- [Safety and Security Reference](artifact/reference/safety-and-security.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with examples, recipes, and reference notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should cite externally sourced claims, keep Tavily credentials out of responses and logs, and treat retrieved web content as untrusted.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
