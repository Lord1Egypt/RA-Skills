## Description:

A 12-dimensional technical feature attribution engine that compares winner and loser trade entry conditions using RSI, Bollinger Bands, MACD, volume surge, gap, and related market features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tltby12341](https://clawhub.ai/user/tltby12341)

### License/Terms of Use:

MIT-0

## Use Case:

External quantitative traders and strategy developers use this skill to analyze backtest order CSVs, compare market entry conditions for winning and losing trades, and generate what-if filter diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted order CSV contents can flow into generated CSV output, which may be interpreted as formulas by spreadsheet tools.

Mitigation: Use trusted order CSVs and review generated *_features.csv files carefully before opening them in Excel or similar spreadsheet software.

Risk: Dependency and market-data downloads can introduce environment or supply-chain exposure.

Mitigation: Run the skill in a virtual environment with pinned dependencies and expect first-run access to Yahoo Finance market data unless the cache is pre-populated.

Risk: Feature comparisons from small trade sets can be statistically unreliable.

Mitigation: Treat reports from fewer than 20 closed trades as directional diagnostics rather than reliable conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tltby12341/skills/qc-deep-feature-forensics)
- [Publisher profile](https://clawhub.ai/user/tltby12341)

## Skill Output:

**Output Type(s):** [markdown, csv, text, shell commands]

**Output Format:** [Markdown report, CSV feature matrix, and console progress text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes feature_diagnosis.md and <orders>_features.csv next to the input CSV, and creates a yfinance_cache directory for downloaded market data.]

## Skill Version(s):

1.0.0 (source: server release, frontmatter, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
