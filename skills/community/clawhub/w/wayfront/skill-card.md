## Description:

Connects an agent to a Wayfront workspace through MCP to query business data such as clients, orders, tickets, subscriptions, invoices, and related records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wayfront-bot](https://clawhub.ai/user/wayfront-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators at agencies use this skill to let an agent inspect Wayfront workspace records and follow relationships across clients, orders, tickets, invoices, subscriptions, templates, team accounts, and logs. The skill helps construct schema-valid MCP queries against the user's authorized Wayfront workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad queries over confidential Wayfront workspace data, including client, billing, support, team, log, template, and activity records.

Mitigation: Install only in a Wayfront workspace where WAYFRONT_MCP_TOKEN is scoped to data the agent is allowed to query, and treat returned business data as confidential.

Risk: The MCP surface is schema-first, so newly exposed tools or endpoints may appear without a skill update.

Mitigation: Review the live tools/list schema and newly exposed MCP tools before using them for broad queries.

## Reference(s):

- [Wayfront homepage](https://wayfront.com)
- [ClawHub skill page](https://clawhub.ai/wayfront-bot/skills/wayfront)
- [ClawHub publisher profile](https://clawhub.ai/user/wayfront-bot)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API call examples]

**Output Format:** [Markdown with JSON examples and inline command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Schema-first guidance; concrete MCP calls should be checked against the live tools/list schema before use.]

## Skill Version(s):

1.0.1 (source: release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
