## Description:

Tigerbrokers helps agents work with the Tiger Brokers OpenAPI Python SDK, CLI, and MCP server for setup, market data, trading workflows, options, real-time push subscriptions, and account queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hotea](https://clawhub.ai/user/hotea)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technically capable traders use this skill to configure Tiger Brokers API access, generate SDK, CLI, and MCP usage guidance, retrieve market data, and draft trading or order-management workflows. Paper trading and read-only modes should be the default unless live financial actions are explicitly requested and confirmed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles brokerage credentials and can guide actions involving real financial accounts.

Mitigation: Install only after review, keep private keys and tokens out of project or synced editor configuration files, and use paper trading plus MCP read-only mode by default.

Risk: Live orders, order changes, cancellations, fund transfers, and forex conversions can affect real funds.

Mitigation: Require explicit human confirmation of account, symbol, action, quantity, price, and account type before any live financial action.

Risk: Examples include confirmation-bypass and unsafe setup patterns.

Mitigation: Avoid -y in agent workflows, pin and review package versions, do not run curl-to-shell installer commands, and never disable TLS verification for real API use.

## Reference(s):

- [Tiger Brokers API Preparation Docs](https://docs.itigerup.com/docs/prepare)
- [Tiger Brokers OpenAPI Python SDK](https://github.com/tigerfintech/openapi-python-sdk)
- [Tiger Brokers Market Data Docs](https://docs.itigerup.com/docs/quote-stock)
- [Tiger Brokers Trading Docs](https://docs.itigerup.com/docs/place-order)
- [Tiger Brokers Options Docs](https://docs.itigerup.com/docs/quote-option)
- [Tiger Brokers Push Quote Docs](https://docs.itigerup.com/docs/push-quote)
- [Tiger MCP Server Docs](https://docs.itigerup.com/docs/mcp)
- [Quickstart Reference](references/quickstart.md)
- [Market Data Reference](references/quote.md)
- [Trading Reference](references/trade.md)
- [Options Reference](references/option.md)
- [Real-time Push Reference](references/push.md)
- [CLI Tool Reference](references/cli.md)
- [MCP Server Reference](references/mcp.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python, shell, JSON, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English and Chinese guidance; live trading, order changes, fund transfers, and forex conversions require explicit human confirmation.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
