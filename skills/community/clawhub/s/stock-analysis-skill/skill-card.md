## Description:

Provides multi-market real-time stock analysis with technical indicators, news sentiment, and AI buy/sell/hold recommendations for portfolios and indices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leohuang8688](https://clawhub.ai/user/leohuang8688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and investment-focused users use this skill to analyze configured portfolios, market indices, or sector watchlists across A-share, Hong Kong, and US markets. It produces technical indicators, news sentiment, and buy/sell/hold reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock symbols, watchlists, and news-search queries may be sent to third-party market and news services.

Mitigation: Configure only the API keys required for the intended workflow, avoid sensitive watchlists, and review the data-provider terms before use.

Risk: Python dependencies are not pinned and the skill depends on live external services that may be delayed, rate-limited, or unavailable.

Mitigation: Install in a virtual environment with normal user privileges, review and pin dependencies, and validate provider limits and data freshness before relying on results.

Risk: Buy/sell/hold outputs are generated from rule-based technical and sentiment scoring and may be inaccurate or incomplete.

Mitigation: Treat outputs as informational analysis, not financial advice, and require human review before making investment decisions.

Risk: Very large stock lists can trigger many outbound requests because no clear per-run request limit is documented.

Mitigation: Keep configured stock lists small or add operational request limits before scheduled or repeated use.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/leohuang8688/skills/stock-analysis-skill)
- [Tavily Search API](https://tavily.com/)
- [Alpha Vantage API](https://www.alphavantage.co/)
- [Tushare Pro](https://tushare.pro/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or Markdown stock-analysis reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes stock recommendations, price levels, confidence, reasoning, sentiment counts, data-source notes, and an investment-risk disclaimer.]

## Skill Version(s):

2.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
