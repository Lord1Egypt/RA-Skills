## Description:

Connects an agent to Robinhood Agentic Trading through MCP to view portfolios, analyze positions, place trades, and run automated trading workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leosaucedo](https://clawhub.ai/user/leosaucedo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent authenticate with Robinhood Agentic Trading, inspect account and market data, and submit or cancel equity orders through Robinhood's MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad financial authority over a dedicated Robinhood Agentic account.

Mitigation: Use only funds you are willing to let an agent manage, apply any available Robinhood spending controls, and revoke access in Robinhood settings when finished.

Risk: Trading commands can execute immediately without an app-side confirmation prompt.

Mitigation: Run review_equity_order before any trade and require human review of order details before calling place_equity_order.

Risk: Read-only Robinhood tools may expose information from all Robinhood accounts.

Mitigation: Install and operate the skill only in environments where account and portfolio data exposure is acceptable.

Risk: Reusable OAuth tokens are stored locally and should be treated as financial credentials.

Mitigation: Set RH_TOKEN_FILE outside repositories and shared folders, add token filenames to gitignore, and protect the token file with restrictive permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leosaucedo/skills/robinhood-agentic)
- [Robinhood Agentic Trading overview](https://robinhood.com/us/en/support/articles/agentic-trading-overview/)
- [Robinhood trading with your agent docs](https://robinhood.com/us/en/support/articles/trading-with-your-agent/)
- [Robinhood Agentic MCP endpoint](https://agent.robinhood.com/mcp/trading)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output from the MCP client]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are command-line oriented; called MCP tools may return plain text or JSON.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and package.json list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
