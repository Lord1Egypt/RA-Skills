## Description:

Trade stocks, options, and crypto on Robinhood using MCP tools or a TypeScript client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevin1chun](https://clawhub.ai/user/kevin1chun)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to inspect Robinhood portfolios, research stocks, options, and crypto, and place or manage trades through an authenticated Robinhood session with required human confirmation for order execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an unpinned third-party package access to Robinhood OAuth tokens, sensitive account data, and live trade execution.

Mitigation: Install only if the package and publisher are trusted, treat outputs as sensitive financial records, avoid logging raw account JSON, and revoke the Robinhood session if package integrity or machine access is uncertain.

Risk: Orders or cancellations could be placed unintentionally.

Mitigation: Require explicit human confirmation after showing account, current price, estimated cost, and order details before each order or cancellation; cancel one order at a time.

Risk: Multiple Robinhood accounts could lead to actions in the wrong account.

Mitigation: Fetch available accounts and ask the user which account to use when more than one account exists.

Risk: Fund transfers or bank operations could move money outside the intended trading workflow.

Mitigation: Refuse deposits, withdrawals, fund transfers, bank unlinking, and bulk cancel operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevin1chun/skills/robinhood-for-agents)
- [Project homepage](https://github.com/kevin1chun/robinhood-for-agents)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, tables, order previews, shell commands, and JSON returned by Robinhood client calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive account, portfolio, order, and session information; avoid logging raw account JSON unless necessary.]

## Skill Version(s):

0.6.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
