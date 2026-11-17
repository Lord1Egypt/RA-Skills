## Description:

Multi-Agent AI Quant System with factor mining, strategy generation, and automated backtesting

This skill is ready for commercial/non-commercial use.

## Publisher:

[pikachu022700](https://clawhub.ai/user/pikachu022700)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to run a multi-agent quantitative research pipeline that collects market data, mines trading factors, generates strategy code, backtests, and returns evaluation metrics for crypto trading strategies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Billing code includes a shared plaintext payment API key and can charge a supplied user ID without a clear confirmation step.

Mitigation: Do not use the billing entrypoint with real user IDs or payment accounts until the publisher removes the embedded key, moves charging to a trusted server-side flow, documents charge timing, and adds explicit confirmation before billing.

Risk: The skill produces trading strategy code and backtest metrics that may be simulated or incomplete.

Mitigation: Review generated strategy code and validate results with independent data and paper trading before any financial use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pikachu022700/skills/quant-orchestrator-free)
- [Quant Orchestrator homepage](https://clawhub.com/quant-orchestrator)
- [Hyperliquid market data API endpoint](https://api.hyperliquid.xyz/info)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands]

**Output Format:** [JSON results, console text, generated strategy code, and markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make network requests for market data and for billing when run through the billing entrypoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
