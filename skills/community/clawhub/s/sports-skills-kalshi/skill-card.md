## Description:

Kalshi prediction markets skill for querying public read-only market data, events, series, trades, and candlestick history for US sports and major soccer leagues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonelli182](https://clawhub.ai/user/antonelli182)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and sports-market analysts use this skill to find open Kalshi markets, inspect event contracts, retrieve market prices as implied probabilities, and review price-history data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kalshi prices can be misread as betting odds or investment recommendations.

Mitigation: Treat prices as market-implied probabilities, not betting or trading advice, and verify any financial decision independently.

Risk: Queries can return stale, closed, or irrelevant markets if required sport or status parameters are omitted.

Mitigation: Pass the documented sport code for sport-specific searches and use status="open" when querying live markets.

## Reference(s):

- [Kalshi API base URL](https://api.elections.kalshi.com/trade-api/v2)
- [API Reference](artifact/references/api-reference.md)
- [Kalshi API](artifact/references/api.md)
- [Valid Commands and Common Mistakes](artifact/references/commands.md)
- [Sport Codes and Series Tickers](artifact/references/series-tickers.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown guidance with CLI commands, Python snippets, and API parameter recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public read-only Kalshi endpoints and does not require credentials for documented read operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
