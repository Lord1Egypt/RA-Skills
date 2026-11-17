## Description:

Quant is an intelligent quantitative investing assistant for multi-source market data retrieval, factor calculation, backtesting, real-time risk checks, and trading signal notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[77spongebob](https://clawhub.ai/user/77spongebob)

### License/Terms of Use:


## Use Case:

Developers and quantitative-investing practitioners use this skill to configure market data access, retrieve stock and index data, calculate factors, run backtests, monitor portfolio risk, and generate trading signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts third-party market data providers and uses a Tushare token while also claiming data is handled locally.

Mitigation: Use a limited-purpose Tushare token, review provider network behavior and terms before use, and do not rely on the local-only privacy statement without verification.

Risk: Dependency installation commands may install market-data and backtesting packages into the agent environment.

Mitigation: Review dependency installation commands before running them and prefer an isolated environment for evaluation.

Risk: Live trading or order-related use could create financial impact if confirmation behavior is unclear.

Mitigation: Avoid connecting the skill to live trading unless the order-confirmation path is explicit, auditable, and tested.

## Reference(s):

- [Quant ClawHub skill page](https://clawhub.ai/77spongebob/skills/quant)
- [Tushare](https://tushare.pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python code, and YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local configuration values, market-data retrieval guidance, backtesting instructions, risk-review guidance, and trading signal descriptions.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-03-08)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
