## Description:

Build production-ready Tavily integrations with best practices baked in. Reference documentation for developers using coding assistants (Claude Code, Cursor, etc.) to implement web search, content extraction, crawling, and research in agentic workflows, RAG systems, or autonomous agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evanydl](https://clawhub.ai/user/evanydl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement Tavily-backed web search, extraction, crawling, URL mapping, research, and framework integrations in agentic workflows, RAG systems, and autonomous agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search, extract, crawl, research, and LLM-verification examples can send prompts, URLs, and retrieved content to external services.

Mitigation: Use only approved Tavily and model-provider environments, and do not send secrets, private URLs, regulated data, or proprietary content unless policy allows it.

Risk: Package installation examples can introduce unreviewed dependency updates into production environments.

Mitigation: Pin and review dependency versions before production use.

Risk: Hybrid RAG examples can persist retrieved web content when foreign-result saving is enabled.

Mitigation: Leave save_foreign disabled unless storing external content is intentional, reviewed, and governed.

Risk: Retrieved web results or synthesized research can be incomplete, stale, or misleading.

Mitigation: Use domain filters, post-filtering, extraction validation, and human review before relying on outputs in downstream workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/evanydl/skills/tavily-bestpractices)
- [SDK Reference](references/sdk.md)
- [Search API Reference](references/search.md)
- [Extract API Reference](references/extract.md)
- [Crawl & Map API Reference](references/crawl.md)
- [Research API Reference](references/research.md)
- [Framework Integrations](references/integrations.md)
- [Tavily Python SDK Reference](https://docs.tavily.com/sdk/python/reference)
- [Tavily JavaScript SDK Reference](https://docs.tavily.com/sdk/javascript/reference)
- [Tavily Search API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/search)
- [Tavily Extract API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/extract)
- [Tavily Crawl API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/crawl)
- [Tavily Integrations Documentation](https://docs.tavily.com/documentation/integrations)
- [Tavily Research Cookbook](https://github.com/tavily-ai/tavily-cookbook/tree/main/research)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python, JavaScript, TypeScript, JSON schema, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory integration guidance for Tavily APIs and related frameworks; users must supply and govern their own API keys, dependencies, and retrieved web content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
