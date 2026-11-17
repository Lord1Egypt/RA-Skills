## Description:

Automated cryptocurrency trading system powered by AI. Instruct the agent to analyze the market and execute Binance spot trades based on technical indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[totoxu](https://clawhub.ai/user/totoxu)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent to analyze Binance cryptocurrency markets and, when configured with exchange credentials, submit Binance spot market orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can charge users and place live Binance market orders with weak confirmation controls.

Mitigation: Use Binance Testnet first, require an explicit preview-and-confirm step before charges or live orders, and avoid production trading until that control exists.

Risk: Exchange credentials and billing credentials can be exposed or over-privileged if configured carelessly.

Mitigation: Restrict Binance API keys to minimum trading permissions, disable withdrawals, prefer IP allowlisting, provide secrets through environment variables, and remove the hardcoded SkillPay key.

Risk: Unpinned dependencies can change behavior or introduce vulnerabilities after installation.

Mitigation: Pin reviewed versions of runtime dependencies such as requests and ccxt before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/totoxu/skills/totoxu-auto-trader)
- [Binance API endpoint used by the artifact](https://api.binance.com/api/v3)
- [SkillPay billing API endpoint used by the artifact](https://skillpay.me/api/v1/billing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external billing, Binance market data, and Binance trading APIs when the user provides required credentials.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
