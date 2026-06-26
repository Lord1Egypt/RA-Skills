## Description: <br>
Trade stocks, options, and crypto on Robinhood using MCP tools or a TypeScript client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevin1chun](https://clawhub.ai/user/kevin1chun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Robinhood portfolios, research securities, and prepare or execute stock, option, and crypto orders with explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live trading operations can create direct financial loss if an order is wrong or unintended. <br>
Mitigation: Require an explicit yes/no confirmation before each trade or cancellation, showing symbol, side, quantity, price, order type, and account. <br>
Risk: Portfolio, account, market, and order outputs can expose private financial data. <br>
Mitigation: Run only on a trusted machine and treat generated output as sensitive financial information. <br>
Risk: The skill depends on an external robinhood-for-agents package and a browser login flow. <br>
Mitigation: Install only if the package is trusted; use the documented OS keychain token storage and re-authenticate when tokens expire. <br>
Risk: Fund transfers, bank operations, and bulk cancellations could create outsized impact. <br>
Mitigation: Refuse fund transfer and bank operation requests, and cancel orders one at a time. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kevin1chun/robinhood-for-agents) <br>
- [Project homepage](https://github.com/kevin1chun/robinhood-for-agents) <br>
- [TypeScript Client API](client-api.md) <br>
- [MCP Tools Reference](reference.md) <br>
- [Authentication Workflow](setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline TypeScript and shell command examples; API responses are typically JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include portfolio, account, market data, order previews, and order-management guidance; trading actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
0.6.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
