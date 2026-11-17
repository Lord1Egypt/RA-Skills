## Description:

Analyzes stock fundamentals such as valuation, profitability, growth, balance-sheet metrics, cash flow, dividends, and analyst targets using Yahoo Finance data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youpele52](https://clawhub.ai/user/youpele52)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and financial-analysis agents use this skill to retrieve a concise fundamentals snapshot for a ticker when they need valuation, profitability, growth, balance-sheet, dividend, analyst-target, and watch-item context beyond a current price quote.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Yahoo Finance through yfinance for each ticker lookup.

Mitigation: Use it only in environments where outbound market-data requests are acceptable, and avoid submitting sensitive or confidential symbols if that disclosure is a concern.

Risk: The skill relies on uv resolving an unpinned yfinance package at runtime.

Mitigation: Pin yfinance to a reviewed version or use a lockfile before deployment in stricter environments.

Risk: The output is market-data-derived analysis and may contain stale, missing, or incomplete values from the upstream data source.

Mitigation: Treat the report as decision support, review N/A values and watch items, and verify material financial decisions against authoritative sources.

## Reference(s):

- [Stock Fundamentals on ClawHub](https://clawhub.ai/youpele52/skills/stock-fundamentals)
- [Yahoo Finance](https://finance.yahoo.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text fundamentals report with labeled sections and bullet lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ticker symbol argument; uses uv to resolve yfinance at runtime; missing market data is rendered as N/A.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
