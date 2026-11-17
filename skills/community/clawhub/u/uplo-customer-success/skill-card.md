## Description:

AI-powered customer success knowledge management. Search account health data, onboarding records, renewal tracking, and support escalation documentation with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Customer success teams and CSMs use this skill to search organization-specific account health, onboarding, renewal, stakeholder, and support escalation knowledge. It supports risk reviews, CSM handoffs, knowledge-gap reporting, outdated-information flagging, and proposed updates grounded in the connected UPLO knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an external MCP package with an API token.

Mitigation: Install only from trusted publishers, pin or otherwise control the MCP server version, and use a narrowly scoped UPLO token.

Risk: The export_org_context workflow can expose broad organization-wide customer-success context.

Mitigation: Restrict bulk export use to authorized roles, confirm scope before running it, and prefer account-scoped searches for routine account reviews or handoffs.

Risk: Customer success records may include confidential contract values, expansion pricing, and restricted account data.

Mitigation: Respect classification tiers and avoid surfacing restricted financial or account details to unauthorized users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/roojenkins/skills/uplo-customer-success)
- [UPLO](https://uplo.ai)
- [UPLO Schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured text with inline tool calls, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account-health summaries, retrieval results, handoff context, knowledge-gap reports, stale-information flags, and proposed knowledge-base updates.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
