## Description:

Statistical Arbitrage 統計套利 helps agents analyze stock pairs with cointegration tests, hedge-ratio calculations, backtesting metrics, and report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loi214](https://clawhub.ai/user/loi214)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request statistical-arbitrage or pairs-trading analysis for listed equities across markets. It is suitable for exploratory analysis and report generation, not automated trading or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented controls may not match executable behavior, which can produce misleading financial analysis.

Mitigation: Review source before installing, run only in an isolated virtual environment, and require fixes for argument parsing, hard-coded securities and dates, readable source, reporting claims, and pinned dependencies before relying on results.

Risk: Outputs may be mistaken for investment advice or reliable trading signals.

Mitigation: Use results only for exploratory analysis, disclose that backtests do not predict future performance, and require qualified review before any trading or investment decision.

Risk: The skill downloads market data and installs Python packages at runtime.

Mitigation: Run with least privilege in a disposable environment, review dependency sources, and avoid using sensitive portfolios or credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loi214/skills/statistical-arbitrage)
- [Publisher profile](https://clawhub.ai/user/loi214)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [requirements.txt](artifact/requirements.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown text with shell commands and generated local report artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce PNG charts, HTML reports, CSV exports, and console metrics when executed.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
