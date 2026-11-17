## Description:

Analyze market sentiment from news articles, social media posts, and financial headlines. Extract bullish/bearish signals, keyword trends, and sentiment scores for Chinese and English markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and trading-tool operators use this skill to summarize market sentiment from financial headlines, public social posts, and news snippets. It supports pre-market checks, position monitoring, earnings-season review, sector comparison, and keyword trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sentiment scores could be mistaken for trading advice or used as the sole basis for market decisions.

Mitigation: Treat scores as informational only, combine them with independent analysis, and avoid using this skill alone for trading decisions.

Risk: Public data-source scraping may conflict with site terms or rely on unstable and noisy source data.

Mitigation: Verify each source's terms and reliability before scraping or operational use.

Risk: Keyword-based sentiment can miss context, sarcasm, new slang, and domain changes.

Mitigation: Maintain the keyword dictionaries regularly and consider validated financial NLP models for production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaocaixia888/skills/zcx-sentiment-analyzer)
- [Sina Finance](https://finance.sina.com.cn/)
- [East Money](https://quote.eastmoney.com/)
- [Weibo hot search endpoint](https://weibo.com/ajax/side/hotSearch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with sentiment summaries, JSON-like analysis objects, Python snippets, and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keyword-based informational sentiment analysis; not trading advice.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
