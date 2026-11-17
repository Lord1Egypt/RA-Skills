## Description:

Stock Trend Scanner scans listed stock symbols with multi-timeframe trend alignment, MACD, volume-price, support and resistance analysis, and composite buy, sell, or hold signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddieguan801-oss](https://clawhub.ai/user/eddieguan801-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run technical scans for named stock symbols and compare heuristic buy, sell, or hold signals based on trend, MACD, volume, and support/resistance indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill emits buy/sell labels that may be mistaken for personalized financial advice.

Mitigation: Present results as heuristic technical-analysis signals and remind users not to treat them as personalized financial advice.

Risk: Market data downloaded through yfinance may be unavailable, delayed, or incomplete.

Mitigation: Ask users for explicit ticker symbols and treat failed or sparse data as a data limitation rather than a recommendation.

## Reference(s):

- [Sample Stock Scanner Output](artifact/references/sample_output.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text console reports with tabular ranking output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language reports; depends on public market data from yfinance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
