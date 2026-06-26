## Description: <br>
Real-time stock and market index quote lookup for A-shares, Hong Kong stocks, and US stocks, with batch query support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuli4](https://clawhub.ai/user/liuli4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up current stock or index quotes by ticker across A-share, Hong Kong, and US markets, including comparing multiple tickers in one request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hong Kong quote lookup may use a local Eastmoney credential and a separate finance-data helper that is not included or pinned in the skill package. <br>
Mitigation: Review the Hong Kong quote path before installation, install only where that helper and credential exposure are trusted, or use a version that documents or removes that path. <br>
Risk: The package is marked as requiring sensitive credentials despite describing itself as needing no API key. <br>
Mitigation: Confirm expected credential behavior during review and avoid deploying it in environments where unintended credential access is unacceptable. <br>


## Reference(s): <br>
- [API reference](references/api-docs.md) <br>
- [Tencent Finance quote API](https://qt.gtimg.cn/q={symbol}) <br>
- [ClawHub release page](https://clawhub.ai/liuli4/stock-price-query-mx) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance for user-facing quote summaries and JSON returned by the stock query script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Batch queries are limited to 20 symbols; script output includes success or error objects per symbol.] <br>

## Skill Version(s): <br>
1.1.4 (source: server evidence and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
