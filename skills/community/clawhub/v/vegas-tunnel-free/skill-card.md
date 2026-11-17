## Description:

维加斯通道交易 helps agents analyze A-share trading scenarios using Vegas tunnel, EMA, Fibonacci retracement, and resonance scoring signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External traders, analysts, and developers use this skill to structure A-share technical analysis, configure market-data inputs, run backtests, and generate trading-signal guidance. Outputs should be reviewed before any live trading or broker-connected workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill discusses API keys and live trading without enough concrete boundaries or safeguards.

Mitigation: Treat the skill as advisory only; require separate explicit approvals and controls before credential use, broker access, or live trading.

Risk: The skill asks for broad execution authority.

Mitigation: Run it in a restricted environment, allow-list permitted commands, and review proposed shell execution before allowing it.

Risk: Trading signals and claimed performance may be inaccurate or unverified.

Mitigation: Independently backtest results, compare against trusted market data, and require human review before financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/vegas-tunnel-free)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Configuration instructions, Shell commands]

**Output Format:** [Markdown with structured JSON examples and trading-signal guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference API keys, market-data sources, and live-trading workflows; requires human review before execution.]

## Skill Version(s):

1.0.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
