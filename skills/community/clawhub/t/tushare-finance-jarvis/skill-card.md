## Description:

获取中国金融市场数据（A股、港股、美股、基金、期货、债券）。支持220+个Tushare Pro接口：股票行情、财务报表、宏观经济指标。当用户请求股价数据、财务分析、指数行情、GDP/CPI等宏观数据时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bingze00000](https://clawhub.ai/user/bingze00000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance analysts use this skill to retrieve Tushare Pro market, fundamentals, fund, futures, bond, and macroeconomic datasets from an agent workflow. It helps users choose documented interfaces, configure credentials, run Python queries, and export results for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tushare API tokens can be exposed if copied into committed files or persistent shell configuration.

Mitigation: Use environment variables or a secrets manager, avoid committing tokens, and review shell configuration before sharing.

Risk: Unpinned dependency ranges may install newer package versions with changed behavior.

Mitigation: Use a virtual environment and pin or review dependency versions before production use.

Risk: Financial market data may be incomplete, delayed, permission-gated, or unsuitable as sole investment advice.

Mitigation: Validate retrieved data against trusted sources and apply domain review before business or trading decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bingze00000/skills/tushare-finance-jarvis)
- [Tushare official documentation](https://tushare.pro/document/2)
- [Tushare API testing tool](https://tushare.pro/document/1)
- [Bundled Tushare interface index](reference/README.md)
- [Bundled API link catalog](reference/all_links.json)
- [Quick reference](QUICK_REFERENCE.md)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, API calls, files]

**Output Format:** [Markdown guidance with Python and shell command examples; API results are typically pandas DataFrames and optional CSV, JSON, or Excel files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Tushare Pro token and Python dependencies such as tushare and pandas.]

## Skill Version(s):

2.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
