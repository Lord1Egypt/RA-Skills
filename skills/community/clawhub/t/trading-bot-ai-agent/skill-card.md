## Description:

Build and evaluate an offline crypto grid-trading simulation without connecting an exchange, wallet, Telegram bot, or user account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frederica123](https://clawhub.ai/user/frederica123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to model hypothetical crypto grid-trading parameters, reserve estimates, and path crossings in an offline simulator. It is intended for scenario analysis and safety review, not investment advice, live trading, custody, or verified performance claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake simplified grid simulations for investment advice, forecasts, backtests, or verified trading performance.

Mitigation: Begin delivered results with a not-investment-advice disclaimer, label outputs as hypothetical scenarios, and state that spread, slippage, latency, funding, partial fills, liquidation, minimum order rules, outages, and tax are excluded.

Risk: Users may provide credentials, wallet secrets, Telegram tokens, or real account details while asking for trading help.

Mitigation: Do not request, repeat, store, or process sensitive values; advise revocation or rotation if a secret was exposed; continue only with non-sensitive hypothetical inputs.

Risk: Users may ask the skill to place orders, connect exchanges or wallets, withdraw assets, export keys, start a Telegram bot, or expose a network service.

Mitigation: Refuse live execution, custody, credential-binding, withdrawal, public-server, and key-export requests, then offer an offline simulation alternative.

## Reference(s):

- [Safety boundaries](references/safety-boundaries.md)
- [ClawHub skill page](https://clawhub.ai/frederica123/skills/trading-bot-ai-agent)
- [Third-party publisher profile](https://clawhub.ai/user/frederica123)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and simulator result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Begins results with a not-investment-advice disclaimer and reports simplified offline grid estimates, optional path simulation, limitations, and one comparison parameter.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
