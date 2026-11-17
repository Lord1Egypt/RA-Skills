## Description:

Collects historical A-share and Hong Kong stock data for one or more specified stocks, supports daily, weekly, monthly, and documented minute-level periods, and exports results as CSV files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang-junjian](https://clawhub.ai/user/wang-junjian)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts can use this skill to collect historical A-share and Hong Kong stock market data for individual tickers or watchlists. It is suited for creating CSV datasets for spreadsheet review, pandas workflows, or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on external Python packages and market data services, so dependency or API changes can affect collection reliability.

Mitigation: Install dependencies in a dedicated virtual environment, consider pinning package versions, and review failed downloads before using generated data.

Risk: Minute-level period options are documented but the security guidance reports they are not implemented correctly.

Mitigation: Use daily, weekly, or monthly periods unless the minute-level behavior is fixed and retested.

## Reference(s):

- [Quickstart Guide](artifact/QUICKSTART.md)
- [ClawHub Skill Page](https://clawhub.ai/wang-junjian/skills/stock-data-collector)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and CSV files produced by the bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated CSV files are written to a configurable output directory and named with stock name, code, market, and period.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
