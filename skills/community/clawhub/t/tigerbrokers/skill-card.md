## Description: <br>
Tigerbrokers helps agents build with Tiger Brokers OpenAPI for SDK setup, market data, trading workflows, real-time push subscriptions, CLI usage, and MCP integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hotea](https://clawhub.ai/user/hotea) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading-tool builders use this skill to configure Tiger Brokers credentials, generate Python, CLI, and MCP examples, query market data, and draft trading workflows for stocks, options, futures, funds, and crypto. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward live brokerage actions such as placing, modifying, or canceling orders, forex orders, and fund transfers. <br>
Mitigation: Keep MCP read-only by default, use paper trading first, and require explicit human confirmation before any live brokerage action. <br>
Risk: Credential examples involve private keys, account identifiers, and 2FA tokens that could be exposed if stored in project or editor configuration files. <br>
Mitigation: Use secure user-level configuration or environment management and never store production private keys or 2FA tokens in project or editor config files. <br>
Risk: Generated trading guidance or code may be incorrect, incomplete, or unsuitable for the user's brokerage account and market permissions. <br>
Mitigation: Review generated code and order details before execution, verify account mode and permissions, and test workflows with paper trading before live use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hotea/tigerbrokers) <br>
- [Tiger Brokers OpenAPI preparation docs](https://docs.itigerup.com/docs/prepare) <br>
- [Tiger Brokers OpenAPI Python SDK](https://github.com/tigerfintech/openapi-python-sdk) <br>
- [Tiger MCP Server docs](https://docs.itigerup.com/docs/mcp) <br>
- [Quickstart](references/quickstart.md) <br>
- [Market Data](references/quote.md) <br>
- [Trading](references/trade.md) <br>
- [Options Trading](references/option.md) <br>
- [Real-time Push](references/push.md) <br>
- [CLI Tool](references/cli.md) <br>
- [MCP Server](references/mcp.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline Python, shell, JSON, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese and English responses; trading guidance should default to paper trading unless the user explicitly requests live trading.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
