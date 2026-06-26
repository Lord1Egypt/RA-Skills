## Description: <br>
悟道 · A股涨停板 helps agents query A-share limit-up market data, including ladders, continuation boards, broken limit-up pools, limit-down pools, approaching limit-up stocks, statistics, hot sectors, event streams, filters, and premium analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcdreamjc](https://clawhub.ai/user/jcdreamjc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer A-share limit-up and short-term board-trading data questions through documented stock.quicktiny.cn OpenClaw endpoints. The returned market analysis should be treated as informational rather than financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an API key for the stock.quicktiny.cn market-data API. <br>
Mitigation: Use a dedicated API key and keep LB_API_KEY out of prompts, logs, and shared transcripts. <br>
Risk: Changing LB_API_BASE could send requests to an unexpected provider. <br>
Mitigation: Keep LB_API_BASE pointed at https://stock.quicktiny.cn/api/openclaw unless the user has explicitly approved a trusted replacement. <br>
Risk: Market analysis returned by the API may be mistaken for financial advice. <br>
Mitigation: Present outputs as informational market data and avoid treating them as recommendations to buy, sell, or hold securities. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jcdreamjc/wudao-limitup) <br>
- [stock.quicktiny.cn market-data service](https://stock.quicktiny.cn) <br>
- [OpenClaw market-data API base](https://stock.quicktiny.cn/api/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with curl examples and JSON response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LB_API_KEY and LB_API_BASE; uses documented read-only market-data endpoints.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
