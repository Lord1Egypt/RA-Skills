## Description:

AI-powered media knowledge management. Search content production records, licensing agreements, distribution data, and audience analytics with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and authorized media operations teams use this skill to search production records, licensing agreements, distribution data, audience analytics, and related organizational context for rights, budget, talent, and performance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad access to organizational media strategy, licensing, budget, talent, and context data can expose sensitive business information.

Mitigation: Install only for authorized users, enforce classification tiers, and use a narrowly scoped, rotatable API token for the configured endpoint.

Risk: The configured MCP server package is run through an unpinned external package command with credentials.

Mitigation: Pin or otherwise verify the MCP server package before use and connect only to a trusted UPLO/AgentDocs endpoint.

Risk: Organization-wide exports or negotiation logging may capture confidential rights, deal, or retention-sensitive material.

Mitigation: Enable exports or negotiation logs only with explicit approval, redaction, retention, and deletion controls.

## Reference(s):

- [Uplo Media on ClawHub](https://clawhub.ai/roojenkins/skills/uplo-media)
- [UPLO](https://uplo.ai)
- [UPLO Schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with MCP tool calls, query examples, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May surface organization-specific media, licensing, budget, talent, and analytics context from the configured UPLO endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
