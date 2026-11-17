## Description:

AI-powered logistics knowledge management. Search shipment records, warehouse procedures, fleet data, and customs documentation with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Operations, logistics, warehouse, fleet, customs, and supply-chain teams use this skill to search organization-specific logistics knowledge, review shipment and carrier information, prepare compliance audits, and surface relevant procedures or directives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can surface sensitive operational, shipment, carrier, customs, and organizational context from connected UPLO knowledge sources.

Mitigation: Use a narrowly scoped UPLO token, enable the skill only for logistics sessions, and require explicit approval before exporting organizational context or logging conversations.

Risk: The MCP server package is invoked through an unpinned external package command.

Mitigation: Confirm the MCP package source and version before installation and monitor updates before use in production logistics environments.

Risk: Actions such as marking records outdated can affect logistics knowledge quality.

Mitigation: Require human review before marking records outdated or making knowledge base updates, especially for contracts, rate sheets, customs classifications, and warehouse procedures.

## Reference(s):

- [Uplo Logistics on ClawHub](https://clawhub.ai/roojenkins/skills/uplo-logistics)
- [UPLO](https://uplo.ai)
- [UPLO Schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline tool calls, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an UPLO instance URL and scoped MCP API token; outputs may include sensitive logistics context from connected knowledge sources.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
