## Description:

Provides three deployable PTrade quantitative trading strategies for small-cap selection, 8-factor scoring with ATR risk controls, and sector rotation with trailing stops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martin-sh-ni](https://clawhub.ai/user/martin-sh-ni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative trading practitioners use this skill to generate or adapt PTrade live-trading scripts for small-cap equity selection, factor scoring with ATR-based risk controls, and ETF sector rotation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill ships automated live-trading scripts whose orders can affect real funds.

Mitigation: Review strategy behavior, run paper trading or backtests, and use explicit human approval before connecting to funded brokerage accounts.

Risk: Server security analysis reports material risk-control and order-state flaws.

Mitigation: Fix the black-swan data-window issue, add broker fill and rejection reconciliation, and enforce aggregate exposure limits before live use.

Risk: Documented schedules and scoring may diverge from the actual strategy code.

Mitigation: Validate rebalance schedules, factor scoring, stop-loss behavior, and position sizing against the code and intended PTrade runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/martin-sh-ni/skills/ptrade-skills)
- [Publisher profile](https://clawhub.ai/user/martin-sh-ni)

## Skill Output:

**Output Type(s):** [Code, Guidance, Configuration]

**Output Format:** [Markdown guidance and Python strategy scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deployable PTrade strategy code that should be reviewed and tested before live trading.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
