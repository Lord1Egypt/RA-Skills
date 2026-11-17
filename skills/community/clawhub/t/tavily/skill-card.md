## Description:

Tavily AI Search helps agents run Tavily Search API queries for web research, current events lookup, domain-specific search, image search, and AI-generated answer summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bert-builder](https://clawhub.ai/user/bert-builder)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to perform Tavily-backed web research, current-events lookup, source filtering, and retrieval of structured results for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and selected search options are sent to Tavily.

Mitigation: Use the skill only when external search disclosure is acceptable, and avoid sending sensitive or confidential queries.

Risk: A Tavily API key can be exposed if passed directly on the command line or stored insecurely.

Mitigation: Store the key in protected configuration or the TAVILY_API_KEY environment variable, and avoid committing real keys or leaving them in shell history.

Risk: The skill depends on the tavily-python package.

Mitigation: Install dependencies in an isolated environment and pin or review package versions before deployment.

## Reference(s):

- [Tavily AI Search on ClawHub](https://clawhub.ai/bert-builder/skills/tavily)
- [Tavily API Reference](references/api-reference.md)
- [Tavily](https://tavily.com)
- [Tavily Documentation](https://docs.tavily.com)
- [Tavily Python SDK](https://github.com/tavily-ai/tavily-python)
- [Tavily Pricing](https://tavily.com/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python examples, and JSON response examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Tavily API key and the tavily-python package; optional settings control search depth, topic, domain filters, images, raw content, and answer generation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
