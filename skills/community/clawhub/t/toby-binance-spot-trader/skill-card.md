## Description:

Autonomous Binance spot trading bot that combines technical indicators and optional LLM sentiment analysis for momentum, mean reversion, and DCA strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to configure and run an automated Binance spot trading agent for selected pairs and strategies. It also provides portfolio tracking and setup guidance for required Binance and SkillBoss credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live automated trading can place unintended Binance spot orders and cause financial loss.

Mitigation: Use withdrawal-disabled, IP-restricted Binance keys on a limited sub-account, start with small funds, and avoid enabling cron or live trading until the safety controls are reviewed.

Risk: Documented DCA intervals, position limits, stop-loss, and take-profit behavior may not be enforced by the code.

Mitigation: Review and test the implementation for those controls before deployment, especially before running unattended.

Risk: LLM sentiment analysis sends trading prompts to SkillBoss when enabled.

Mitigation: Disable USE_LLM unless sharing market and trading-context prompts with SkillBoss is acceptable.

## Reference(s):

- [Binance REST API Reference](references/binance-api.md)
- [Technical Indicators](references/indicators.md)
- [Publisher profile](https://clawhub.ai/user/tobeyrebecca)
- [Skill page](https://clawhub.ai/tobeyrebecca/skills/toby-binance-spot-trader)
- [Homepage](https://github.com/srikanthbellary)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with shell commands, environment-variable configuration, and Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Binance API credentials and a SkillBoss API key; live trading can place market orders.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
