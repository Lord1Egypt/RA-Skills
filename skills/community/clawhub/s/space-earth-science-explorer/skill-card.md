## Description:

Space & Earth Science Explorer searches and retrieves space imagery, scientific datasets, earthquake events, and earth observation data through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and researchers use this skill to query NASA, NOAA, USGS, and data.gov sources for space imagery, climate and earth observation datasets, earthquake events, and related science records. It supports natural-language queries with source, time-period, magnitude, and result-limit controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned remote setup commands can install a changed upstream package or skill state.

Mitigation: Prefer ClawHub-managed or otherwise pinned installation routes, and verify the current source before running unpinned npx setup commands.

Risk: The generic activation keyword can cause unintended automatic skill selection.

Mitigation: Review automatic skill-selection settings and require explicit use of the Space Earth Science Explorer action for sensitive workflows.

Risk: Prompts or logs can expose secrets or sensitive account details if users include them while configuring AgentPMT access.

Mitigation: Use the referenced setup skills for credential handling and keep prompts free of account secrets, wallet private keys, mnemonics, signatures, and payment headers.

Risk: The artifact says to reinstall if more than seven days have passed since its 2026-06-24 update date before relying on endpoints, schemas, setup steps, or examples.

Mitigation: Refresh the skill from ClawHub or the approved installation route before production use when endpoint or schema freshness matters.

## Reference(s):

- [Space Earth Science Explorer marketplace page](https://www.agentpmt.com/marketplace/space-earth-science-explorer)
- [Space Earth Science Explorer ClawHub page](https://clawhub.ai/agentpmt/skills/space-earth-science-explorer)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)
- [Local generated action schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown guidance with JSON request examples and JSON result records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include source, kind, agency, title, description, source-specific metadata, and an errors array for partial upstream failures.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
