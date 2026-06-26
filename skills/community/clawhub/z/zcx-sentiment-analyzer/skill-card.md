## Description: <br>
Analyze market sentiment from news articles, social media posts, and financial headlines. Extract bullish/bearish signals, keyword trends, and sentiment scores for Chinese and English markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to summarize market mood from financial headlines, public posts, and news snippets before trading research or portfolio monitoring. It provides keyword-based bullish, bearish, neutral, and trend summaries for Chinese and English market text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill produces rough keyword-based sentiment summaries that can be mistaken for investment advice. <br>
Mitigation: Present results as informational analysis only and require users to validate conclusions with independent financial research. <br>
Risk: Public market pages fetched with curl may be unavailable, incomplete, or structurally different from the examples. <br>
Mitigation: Check fetched content before relying on summaries and treat missing or malformed source data as inconclusive. <br>
Risk: Keyword dictionaries can miss context, sarcasm, new slang, and domain-specific meaning. <br>
Mitigation: Review matched keywords and update dictionaries for the target market, language, and time period. <br>


## Reference(s): <br>
- [Sentiment Analyzer on ClawHub](https://clawhub.ai/zhaocaixia888/zcx-sentiment-analyzer) <br>
- [Publisher profile: zhaocaixia888](https://clawhub.ai/user/zhaocaixia888) <br>
- [Sina Finance](https://finance.sina.com.cn/) <br>
- [East Money](https://quote.eastmoney.com/) <br>
- [Weibo hot search API](https://weibo.com/ajax/side/hotSearch) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks, sentiment scores, keyword lists, and short market sentiment reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Keyword-based analysis only; outputs are informational and not financial advice.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
