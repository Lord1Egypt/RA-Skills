## Description: <br>
Automated cryptocurrency trading system powered by AI. Instruct the agent to analyze the market and execute Binance spot trades based on technical indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[totoxu](https://clawhub.ai/user/totoxu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to request Binance market analysis and, when authorized, place spot buy or sell orders with user-supplied Binance credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live Binance spot trades with real funds when production API keys are supplied. <br>
Mitigation: Use Binance testnet first, require manual confirmation for every live order, and use a dedicated trade-only API key with withdrawals disabled, IP restrictions enabled, and limited funds available. <br>
Risk: Billing defaults and SkillPay configuration need review before user IDs or credentials are passed to the scripts. <br>
Mitigation: Verify the SkillPay configuration and billing behavior before use, and stop execution when a payment URL or billing error is returned. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/totoxu/totoxu-auto-trader) <br>
- [Binance API endpoint used for market data](https://api.binance.com/api/v3) <br>
- [SkillPay billing endpoint](https://skillpay.me/api/v1/billing) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands; invoked scripts return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a billing user ID. Live trading requires BINANCE_API_KEY and BINANCE_SECRET environment variables.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
