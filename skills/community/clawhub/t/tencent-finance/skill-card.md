## Description:

腾讯财经行情接口用于通过腾讯财经公开接口查询 A 股、港股、美股指数、期货、外汇和 ETF 的实时行情数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ezio-xiang](https://clawhub.ai/user/ezio-xiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent builders use this skill to retrieve and format real-time market quote data for supported stock, index, commodity, forex, and ETF symbols. Outputs are suitable for interactive lookups or scheduled quote snapshots, but should be treated as informational rather than investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticker symbols or code lists are sent to Tencent's finance endpoint during quote retrieval.

Mitigation: Avoid including personal portfolio notes, trading strategy text, or other sensitive context in ticker arguments.

Risk: Returned market data may be incomplete, delayed, unavailable, or unsuitable as a basis for financial decisions.

Mitigation: Treat returned quotes as informational only and verify important data against authoritative market-data sources before acting on it.

Risk: High-frequency polling can trigger endpoint throttling or IP blocking.

Mitigation: Keep requests at least 100 ms apart or use a more conservative rate limit for automated and cron-based retrieval.

## Reference(s):

- [Tencent Finance quote endpoint](https://qt.gtimg.cn/q=)
- [ClawHub skill page](https://clawhub.ai/ezio-xiang/skills/tencent-finance)
- [Publisher profile](https://clawhub.ai/user/ezio-xiang)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with Python examples and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries Tencent's public finance endpoint and formats selected quote fields such as price, open, high, low, volume, turnover, PE, and percentage change.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
