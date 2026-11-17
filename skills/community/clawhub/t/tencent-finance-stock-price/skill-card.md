## Description:

Queries real-time stock data from the Tencent Finance API for Chinese A-shares, Hong Kong stocks, and US stocks, including price, change, market capitalization, valuation ratios, volume, turnover, shares, and 52-week range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangzhe1991](https://clawhub.ai/user/yangzhe1991)

### License/Terms of Use:

MIT-0

## Use Case:

Agents supporting analysts, developers, or finance-oriented users can use this skill to fetch quote snapshots and market metrics for supported A-share, Hong Kong, US stock, and index symbols. Results are informational and should be verified before financial decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried stock symbols are sent to Tencent Finance over plaintext HTTP.

Mitigation: Use only when plaintext quote lookups are acceptable and avoid submitting sensitive watchlists or symbols.

Risk: Stock prices and financial metrics may be unauthenticated, stale, incomplete, or unsuitable for trading decisions.

Mitigation: Treat results as informational and verify prices and metrics with an authenticated financial data source before making financial decisions.

Risk: Parts of the command-line output are in Chinese.

Mitigation: Confirm downstream users or agents can interpret the Chinese labels before relying on the output in workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangzhe1991/skills/tencent-finance-stock-price)
- [Tencent Finance quote endpoint](http://qt.gtimg.cn/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text output in compact or detailed tabular form]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports compact and detail modes; some command-line output is in Chinese.]

## Skill Version(s):

2.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
