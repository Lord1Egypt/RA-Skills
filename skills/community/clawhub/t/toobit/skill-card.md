## Description: <br>
Trade crypto on Toobit exchange via natural language. Spot & USDT-M futures trading, market data queries, wallet management. Use when user mentions Toobit, or wants to trade/query crypto on Toobit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuxizhen](https://clawhub.ai/user/xuxizhen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Toobit market, account, wallet, spot trading, and USDT-M futures endpoints from natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use exchange API keys for financially sensitive actions including trades, cancellations, leverage changes, transfers, and withdrawals. <br>
Mitigation: Install only when an agent should operate a Toobit account, use a dedicated restricted API key, disable withdrawals unless required, and enable IP restrictions when available. <br>
Risk: Incorrect symbols, sides, amounts, prices, leverage values, cancellation scopes, destination addresses, or generated commands can cause unwanted financial outcomes. <br>
Mitigation: Manually verify each parameter and command before confirming any write action, and require explicit confirmation for withdrawals. <br>


## Reference(s): <br>
- [Toobit API base URL](https://api.toobit.com) <br>
- [ClawHub skill page](https://clawhub.ai/xuxizhen/toobit) <br>
- [Publisher profile](https://clawhub.ai/user/xuxizhen) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions, Markdown] <br>
**Output Format:** [Markdown with inline bash and curl commands plus readable summaries of JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require TOOBIT_API_KEY and TOOBIT_API_SECRET for signed exchange operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
