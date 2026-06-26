## Description: <br>
美股行情与舆情监控工具，支持 Yahoo Finance 行情查询、Google News RSS 新闻检索和 X/Twitter 舆情监控。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gold3bear](https://clawhub.ai/user/gold3bear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check U.S. stock indices, futures, major technology stocks, macro rates, and recent market sentiment when answering market-monitoring questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker symbols and market questions may be sent to public finance, news, and social-search services. <br>
Mitigation: Use the skill only when that external sharing is acceptable, and avoid submitting confidential trading plans or private portfolio details. <br>
Risk: Market outputs can be delayed, incomplete, or unsuitable as financial advice. <br>
Mitigation: Treat results as informational market data and verify important figures with authoritative sources before acting. <br>
Risk: Running the scripts depends on local Python packages and public web endpoints. <br>
Mitigation: Review and verify dependencies before execution, and expect graceful degradation when external services are unavailable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gold3bear/us-stock-radar-gold3bear) <br>
- [NY Fed latest reference rates API](https://markets.newyorkfed.org/api/rates/all/latest.json) <br>
- [Yahoo Finance quote endpoint](https://query1.finance.yahoo.com/v7/finance/quote) <br>
- [FRED graph CSV endpoint](https://fred.stlouisfed.org/graph/fredgraph.csv) <br>
- [Google News RSS search](https://news.google.com/rss/search) <br>
- [X search](https://x.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal text with market quotes, headlines, sentiment prompts, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live market prices, percentage changes, macro-rate values, links to public data sources, and informational market commentary.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
