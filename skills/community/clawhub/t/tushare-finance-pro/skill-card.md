## Description: <br>
Tushare Pro 金融数据接口 - A股/港股/美股/基金/期货/债券/宏观经济，220+数据接口，支持财务报表、估值分析、行业研究 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhaofeng-max](https://clawhub.ai/user/wangzhaofeng-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve Tushare Pro financial market data and produce financial data queries, reports, valuation examples, and OpenClaw automation snippets for market research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tushare API token exposure <br>
Mitigation: Use environment variables or a secret manager, scope the token to the current session when possible, and do not commit token-bearing config files. <br>
Risk: Outbound financial-data requests may disclose query intent or depend on third-party availability. <br>
Mitigation: Run only in environments approved for Tushare access and handle API failures, delays, and rate limits in downstream workflows. <br>
Risk: Financial data and generated valuation examples may be stale or unsuitable for investment decisions. <br>
Mitigation: Treat outputs as research support, verify data against authoritative sources, and avoid presenting results as investment advice. <br>
Risk: Helper tests or logs can expose token values if examples are modified carelessly. <br>
Mitigation: Remove token-printing lines and avoid shared logs when validating connectivity. <br>


## Reference(s): <br>
- [ClawHub release: Tushare 金融数据助手](https://clawhub.ai/wangzhaofeng-max/tushare-finance-pro) <br>
- [Tushare Pro](https://tushare.pro) <br>
- [Tushare Pro documentation](https://tushare.pro/document/2) <br>
- [Artifact README](artifact/README.md) <br>
- [Quick reference](artifact/QUICK_REFERENCE.md) <br>
- [Bundled API reference index](artifact/reference/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python, JSON, YAML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce pandas DataFrame-oriented examples and OpenClaw cron configuration snippets; requires a user-provided Tushare token for live API use.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
