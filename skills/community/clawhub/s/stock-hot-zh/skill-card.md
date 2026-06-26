## Description: <br>
通过 AISA 扫描热门股票和加密资产的实时异动，帮助用户了解当前热门、波动明显、动量突出或消息驱动的市场标的。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market-focused agents use this skill to request real-time summaries of active stocks and crypto assets, including movers, volume activity, news catalysts, watchlist candidates, and a concise market take. The output is informational and not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends market-scanning prompts to an external AISA API using a user-provided AISA_API_KEY. <br>
Mitigation: Use only with a trusted AISA endpoint, protect the API key, and avoid sending confidential trading strategies or sensitive account details. <br>
Risk: Stock and crypto market summaries may be incomplete, stale, or unsuitable for financial decisions. <br>
Mitigation: Treat the report as informational, verify material claims with trusted market data sources, and do not use it as investment advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/stock-hot-zh) <br>
- [AISA API endpoint](https://api.aisa.one/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown market report with optional JSON summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; supports focus on stocks, crypto, or both.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
