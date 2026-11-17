## Description:

Analyzes China A-share stocks with real-time quotes, technical indicators, quantitative screening, risk checks, market sentiment, and buy/sell-style signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxie48892-jpg](https://clawhub.ai/user/dxie48892-jpg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to query China A-share symbols, calculate common technical indicators, screen candidate stocks, check risk flags, and generate structured trading analysis for educational review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce action-oriented stock guidance from public finance APIs and fallback or sample data.

Mitigation: Treat outputs as educational analysis only and verify any trading decision with trusted, current financial data.

Risk: Public Tencent/Sina finance API responses may be incomplete, unavailable, or stale.

Mitigation: Check for returned errors or fallback values and compare against an authoritative market data source before relying on the analysis.

Risk: Quantitative screening may use hard-coded sample fundamentals rather than complete live company datasets.

Mitigation: Confirm fundamentals such as PE, ROE, revenue growth, and leverage from a reliable financial database before acting on screening results.

## Reference(s):

- [Quant Trading Assistant on ClawHub](https://clawhub.ai/dxie48892-jpg/skills/quant-trading-assistant)
- [Publisher profile](https://clawhub.ai/user/dxie48892-jpg)
- [Tencent Finance quote API](https://qt.gtimg.cn/q={symbol})
- [Sina Finance K-line API](https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={sina_sym}&scale={scale}&ma=no&datalen={datalen})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown explanations and JSON/code snippets with optional shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include action-oriented trading guidance that should be verified against trusted financial data sources.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
