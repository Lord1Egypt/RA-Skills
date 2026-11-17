## Description:

Weather Trader helps an agent scan and trade weather temperature prediction markets on Polymarket through the Simmer SDK using NOAA and Open-Meteo forecasts, expected-value checks, Kelly sizing, Bayesian position updates, and maker/taker strategy switching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhlorra](https://clawhub.ai/user/yhlorra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze weather-market opportunities, configure trading thresholds, size positions, execute or simulate trades, and review weather trading performance. It is intended for agents operating weather prediction-market workflows where real-money trading risk may apply.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real USDC trades when live trading is enabled.

Mitigation: Audit the effective configuration first, start with dry-run or Simmer virtual trading, and avoid live mode until position limits, venue settings, and safeguards are understood.

Risk: Security evidence reports broad local code-loading behavior that is too broad for automatic trust.

Mitigation: Run the skill only from a trusted, isolated skill directory and avoid shared directories where sibling files could influence imports.

Risk: An unpinned or unexpected Simmer SDK dependency could change runtime behavior.

Mitigation: Pin and review the installed simmer-sdk version before deployment.

Risk: Disabling safeguards can bypass controls such as slippage checks and circuit-breaker behavior.

Mitigation: Keep safeguards enabled for normal use and reserve --no-safeguards for audited, deliberate maintenance or testing scenarios.

## Reference(s):

- [Weather Trader on ClawHub](https://clawhub.ai/yhlorra/skills/yh-polymarket-weather-trader)
- [Publisher profile: yhlorra](https://clawhub.ai/user/yhlorra)
- [Simmer API](https://api.simmer.markets)
- [Simmer Dashboard](https://simmer.markets/dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with inline commands, configuration values, trading analysis, and status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May place API-backed simulated or real trades when configured and invoked with live trading options.]

## Skill Version(s):

1.16.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
