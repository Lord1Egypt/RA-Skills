## Description:

Synthetic Data Generator: Generate synthetic test data: persons, companies, families, e-commerce, auth systems, CRM, financial, technical IDs. 10 locales, edge cases, deterministic seeding. Use when an agent needs synthetic data generator, generate realistic customer data, usage patterns, and transaction history, edge cases to validate ui robustness, generate, data type, count through AgentPMT-hosted remote tool calls. Discovery terms: synthetic data generator, generate realistic customer data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and agents use this skill to generate realistic fake persons, companies, families, financial records, technical identifiers, and relational datasets for testing, prototyping, demonstrations, validation, and stress testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses AgentPMT-hosted remote service calls, so prompts or tool inputs may be sent outside the local agent environment.

Mitigation: Use the skill only when the AgentPMT hosted service is intended, keep inputs scoped to the minimum needed, and do not send real secrets, wallet material, payment headers, or production personal data.

Risk: Setup instructions include install routes that may change over time or rely on unpinned commands.

Mitigation: Prefer OpenClaw or pinned and verified setup paths, and refresh the skill before production integration when schemas, endpoints, or examples are stale.

Risk: Generated financial, technical, and edge-case values may resemble sensitive or attack-oriented data and can be misused if confused with real production records.

Mitigation: Treat generated values as test fixtures only, label them clearly in downstream systems, and use edge-case or injection-pattern outputs only in controlled validation environments.

## Reference(s):

- [Synthetic Data Generator Schema](artifact/schema.md)
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/synthetic-data-generator)
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/synthetic-data-generator)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Configuration instructions]

**Output Format:** [JSON responses from AgentPMT-hosted remote tool calls, with Markdown guidance and JSON examples in the skill instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports nine data types, 10 locales, deterministic seeding, edge-case generation, and dataset sizes from small to large.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
