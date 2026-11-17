## Description:

帮助用户按分层信号源扫描美股 IPO、新股、直接上市和相关基金机会，并整理早期关注线索。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aidalong](https://clawhub.ai/user/aidalong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to monitor public IPO, new-listing, stock-news, and market-sentiment sources for early research leads. Outputs should support further investigation, not replace independent market-data verification or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-monitoring output may be mistaken for financial advice.

Mitigation: Treat output as research prompts and independently confirm market data before making investment decisions.

Risk: Public news, RSS, and social sentiment sources can be noisy, delayed, incomplete, or promotional.

Mitigation: Use the layered signals as leads and require deeper research before taking action.

## Reference(s):

- [美股IPO信号源详细列表](references/sources.md)
- [ClawHub skill page](https://clawhub.ai/aidalong/skills/us-stock-ipo-scanner)
- [Invezz IPO feed](https://invezz.com/news/stocks/ipos/feed/)
- [Nasdaq IPO calendar](https://www.nasdaq.com/market-activity/ipos)
- [CNBC IPO news RSS](https://www.cnbc.com/id/100003114/device/rss/rss.html)
- [Seeking Alpha IPO market news](https://seekingalpha.com/market-news/ipos.xml)
- [Benzinga market news feed](https://www.benzinga.com/feed)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown scanning report with discovered tickers or funds, source notes, signal checks, market-sentiment context, and follow-up research suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research-oriented output; investment decisions require independent market-data confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
