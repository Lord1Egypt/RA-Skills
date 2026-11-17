## Description:

AI-powered customer lifecycle intelligence spanning sales, customer success, and retail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Revenue, customer success, sales, and retail operations teams use this skill to search customer lifecycle knowledge, prepare account reviews, investigate churn signals, and identify opportunities across sales history, support activity, product usage, and retail data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A mutable third-party MCP package and API token are required to connect the agent to UPLO.

Mitigation: Review or pin the MCP server package version, use a least-privilege UPLO token, and rotate credentials according to organizational policy.

Risk: Broad customer and organizational search or export operations may expose confidential account, pricing, support, or revenue data.

Mitigation: Restrict access to assigned accounts and approved datasets, preserve classification tiers, and treat exports and broad searches as confidential.

Risk: Customer lifecycle answers may be incomplete or stale when source systems lack current account notes, QBR records, support history, or directives.

Mitigation: Use the skill's gap and outdated-content reporting workflows, and verify high-impact customer decisions against authoritative systems.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/roojenkins/skills/uplo-customer-360)
- [Publisher profile](https://clawhub.ai/user/roojenkins)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration, and natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include customer/account summaries, search queries, workflow steps, risk flags, and MCP configuration guidance; customer exports and broad searches should be treated as confidential.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
