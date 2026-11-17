## Description:

Route every task to the best MCP server and cheapest LLM. Scores on real execution data across quality, reliability, speed, cost, and trust.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grossiweb](https://clawhub.ai/user/grossiweb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use ToolRoute to request routing recommendations for MCP servers, LLM models, and fallback chains before executing a task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task descriptions are sent to an external ToolRoute service before use.

Mitigation: Use generalized task descriptions and remove confidential, legal, financial, security, customer, source-code-sensitive, identifying, or credential material before routing.

Risk: The skill asks agents to follow externally recommended tools or models without clear local limits.

Mitigation: Review the recommended MCP server, model, and fallback chain before execution, especially for sensitive or high-impact work.

Risk: Optional registration, reporting, social verification, and npm package installation can add tracking or supply-chain exposure.

Mitigation: Treat those features as optional and enable them only after manual approval of the outbound text, dependency source, and credential storage location.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/grossiweb/skills/toolroute)
- [ToolRoute API Docs](https://toolroute.io/api-docs)
- [ToolRoute Server Catalog](https://toolroute.io/servers)
- [ToolRoute Model Catalog](https://toolroute.io/models)
- [ToolRoute Privacy Policy](https://toolroute.io/privacy)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl. Normal use sends generalized task descriptions and optional execution metadata to ToolRoute.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter lists 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
