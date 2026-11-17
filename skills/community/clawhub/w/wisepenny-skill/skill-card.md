## Description:

Analyze and organize personal or household finances through Wise Penny, an MCP server connected read-only via Plaid to the user's bank accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ottowatt](https://clawhub.ai/user/ottowatt)

### License/Terms of Use:

MIT-0

## Use Case:

External users connect Wise Penny to an assistant so it can summarize balances, transactions, spending, cash flow, budgets, savings goals, recurring bills, and account organization. The skill helps users review where money goes, identify upcoming bills or subscriptions, assess net worth, and propose user-directed organization changes such as categories, tags, splits, rules, budgets, goals, and transfer links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive financial account data to an assistant for reading and summarization.

Mitigation: Install only when the user is comfortable connecting Wise Penny through Plaid and allowing the assistant to read and summarize that data.

Risk: User-approved deletes, rule changes, and organization updates can persist in the Wise Penny account.

Mitigation: Review proposed writes before approval, use clear prompts, and take extra care with deletes or rule changes.

Risk: Financial summaries can be affected by stale, partial, or disconnected account data.

Mitigation: Check connection health and data quality before presenting figures, and caveat numbers when source data is stale or incomplete.

## Reference(s):

- [Wise Penny Skill Source](https://github.com/ottowatt/wisepenny-skill)
- [Wise Penny App](https://www.wisepenny.app)
- [Wise Penny MCP Server](https://www.wisepenny.app/api/mcp)
- [Connect AI Help](https://www.wisepenny.app/help/connect-ai)
- [ClawHub Skill Page](https://clawhub.ai/ottowatt/skills/wisepenny-skill)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with concise summaries, recommendations, and inline shell commands for MCP setup when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user-directed proposals for reversible transaction edits or persistent Wise Penny organization changes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
