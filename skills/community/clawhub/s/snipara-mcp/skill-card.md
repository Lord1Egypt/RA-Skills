## Description:

Semantic search tool to quickly find answers across multiple code repositories with AI memory of user preferences for faster documentation lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alopez3006](https://clawhub.ai/user/alopez3006)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use Snipara MCP to let agents query indexed documentation, search across repositories, manage shared context, and recall approved preferences while answering codebase questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send selected documentation, queries, preferences, summaries, and agent coordination data to Snipara.

Mitigation: Avoid secrets or regulated data, index only approved documents, and use least-privilege project credentials.

Risk: Returned templates, shared context, memories, or search results may be surfaced to the agent as guidance.

Mitigation: Treat returned content as untrusted reference material and review it before acting on instructions or generated changes.

Risk: Document sync and delete-capable workflows can alter indexed project documentation.

Mitigation: Review sync and delete operations before allowing them, and keep source documentation backed by version control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alopez3006/skills/snipara-mcp)
- [Snipara documentation](https://docs.snipara.com)
- [Snipara website](https://snipara.com)
- [PyPI package](https://pypi.org/project/snipara-mcp/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with JSON arguments and shell or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include queried documentation excerpts, memory results, shared context, and tool outputs returned by Snipara services.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
