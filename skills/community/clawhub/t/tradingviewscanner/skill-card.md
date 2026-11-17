## Description:

Scans stock watchlists with TradingView market data, computes technical indicators across A-share, Hong Kong, U.S., and Japanese markets, and generates Markdown reports with optional Excel output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sarahwang94712](https://clawhub.ai/user/sarahwang94712)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run batch technical analysis on watchlist tickers and create daily reports in an Obsidian vault. The generated reports support review of market signals and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local watchlists and sends ticker symbols to TradingView.

Mitigation: Run it only on watchlists whose ticker contents may be shared with TradingView, and avoid including private notes or unnecessary columns in the input CSV.

Risk: The setup guidance includes risky dependency installation flags.

Mitigation: Install dependencies in a virtual environment, avoid sudo, and do not use --break-system-packages unless the environment owner has approved it.

Risk: The skill writes Markdown and optional Excel reports into a local vault.

Mitigation: Confirm output paths before execution, treat imported watchlists as untrusted input, and review generated Excel files before sharing or opening in sensitive environments.

Risk: Recurring scheduled execution can repeatedly read local files and write reports.

Mitigation: Review any cron entry before adding it, use explicit absolute paths, and disable the schedule when the scanner is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sarahwang94712/skills/tradingviewscanner)
- [Sample technical scan report](artifact/sample_report.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown reports with optional Excel files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a watchlist CSV, sends ticker symbols to TradingView, and writes reports to a user-selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
