## Description:

Validates historical behavior of stock ranking, factor, and portfolio-selection strategies using reproducible backtests, benchmark comparison, turnover, drawdown, and bias warnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teahann](https://clawhub.ai/user/teahann)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users use this skill to evaluate historical behavior for equity ranking, factor, or portfolio-selection strategies from local signal and price CSV files. It helps report setup, performance, benchmark context when available, robustness warnings, confidence, and data gaps before a strategy is used elsewhere.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CSV reports may include ticker values from untrusted input and can be unsafe when opened in spreadsheet tools with formula execution enabled.

Mitigation: Use trusted signal CSVs and open generated CSV outputs with spreadsheet formula execution disabled or in a plain-text viewer.

Risk: Backtest results can be mistaken for forecasts or trading instructions.

Mitigation: Present results as historical simulations only, keep assumptions visible, and avoid absolute buy or sell recommendations.

Risk: Benchmark and bias review may require manual work beyond the bundled script.

Mitigation: Manually review benchmark availability, survivorship bias, lookahead bias, data-snooping risk, liquidity assumptions, and fee or slippage sensitivity before relying on the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teahann/skills/strategy-backtester)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown report with optional shell commands plus generated JSON and CSV backtest files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local CSV inputs; generated results are historical simulations, not forecasts or trading instructions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
