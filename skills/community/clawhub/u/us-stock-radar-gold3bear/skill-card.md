## Description:

Monitors U.S. stock indices, futures, major technology stocks, macro rates, and market news and social signals using public finance and news sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gold3bear](https://clawhub.ai/user/gold3bear)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve U.S. market snapshots, macro-rate context, and manual news and social lookup links for market monitoring and short-form commentary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled use can create repeated outbound requests to public finance, news, and social sites.

Mitigation: Run the skill on demand or schedule checks conservatively, and review the relevant data-source terms and operational limits before recurring use.

Risk: News and X/Twitter links are manual lookup aids, not a complete sentiment-analysis system.

Mitigation: Treat headlines and social posts as unverified signals and corroborate market-moving claims with reliable sources before acting on them.

Risk: Market data can be delayed, unavailable, or incomplete during source outages or rate limits.

Mitigation: Use the output as monitoring context rather than financial advice, and confirm critical values with authoritative market-data sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gold3bear/skills/us-stock-radar-gold3bear)
- [NY Fed latest reference rates API](https://markets.newyorkfed.org/api/rates/all/latest.json)
- [FRED graph CSV endpoint](https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&vintage_date={date})
- [Yahoo Finance chart endpoint](https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d)
- [Google News RSS market search](https://news.google.com/rss/search?q=US+stock+market+when:1h)
- [X live market search](https://x.com/search?q=%24NVDA+%24TSLA+stock&f=live)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Chinese-language terminal text and concise market-monitoring guidance with runnable Python commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public outbound requests to finance, news, and social sites; no credential inputs are described.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
