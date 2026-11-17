## Description:

Hire Spanish-speaking humans for real-world tasks in Latin America. Create missions, browse humans, manage payments, reviews, and disputes through 15 MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gymtopz](https://clawhub.ai/user/gymtopz)

### License/Terms of Use:


## Use Case:

External developers and operators use this skill to connect agents to RentaUnHumano MCP tools for creating, tracking, and resolving real-world human tasks in Latin America.

### Deployment Geography for Use:

Latin America

## Known Risks and Mitigations:

Risk: The skill can create paid, location-based real-world tasks when used with a live API key.

Mitigation: Use sandbox mode first and require operator confirmation for spending and task creation before production use.

Risk: The setup runs an unpinned external MCP package with an API key.

Mitigation: Pin and verify the MCP server package version, and use a narrowly scoped, revocable API key.

Risk: Missions, messages, proof files, reviews, and disputes may disclose sensitive personal or business information to the service or assigned workers.

Mitigation: Avoid submitting secrets, credentials, unnecessary personal data, regulated data, or sensitive business details unless disclosure is intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gymtopz/skills/rentaunhumano-mcp)
- [RentaUnHumano Platform](https://rentaunhumano.com)
- [RentaUnHumano API Docs](https://rentaunhumano.com/docs/api)
- [RentaUnHumano MCP Docs](https://rentaunhumano.com/docs/mcp)
- [OpenAPI Spec](https://rentaunhumano.com/.well-known/openapi.yaml)
- [npm Package](https://www.npmjs.com/package/@rentaunhumano/mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger MCP API actions that create paid, location-based real-world tasks when configured with a live API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
