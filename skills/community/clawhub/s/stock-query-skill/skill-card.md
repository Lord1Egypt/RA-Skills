## Description:

Stock Query Skill helps agents query the past 30 days of daily stock-price data for a supplied ticker and save the returned market data as a CSV file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tf9527666666-spec](https://clawhub.ai/user/tf9527666666-spec)

### License/Terms of Use:

MIT-0

## Use Case:

Agents assisting developers, analysts, or operations users can use this skill to fetch recent daily OHLCV data for a stock ticker through yfinance and produce a CSV file for inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts market-data services through yfinance.

Mitigation: Run it only in environments where outbound market-data access is expected and approved.

Risk: The script creates a CSV file in the current working directory.

Mitigation: Run it from an isolated workspace or disposable directory and review generated files before reuse.

Risk: The dependency set includes yfinance and pandas without pinned reviewed versions in the artifact.

Mitigation: Install dependencies in an isolated virtual environment and pin reviewed package versions before deployment.

Risk: The security guidance notes that the current script appears to need a syntax fix before it will run.

Mitigation: Review and test the script before relying on generated stock-price output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tf9527666666-spec/skills/stock-query-skill)
- [Artifact README](artifact/README.md)
- [Artifact SKILL](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Markdown guidance with command examples and CSV file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a ticker-named CSV file in the current working directory and uses yfinance for market-data retrieval.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
