## Description:

Tushare Pro 金融数据接口助手，支持 A 股、港股、美股、基金、期货、债券和宏观经济数据查询，并提供财务报表、估值分析和行业研究支持。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhaofeng-max](https://clawhub.ai/user/wangzhaofeng-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and finance workflow builders use this skill to retrieve Tushare Pro market, financial statement, fund, futures, bond, and macroeconomic data. It helps agents draft code, shell commands, configuration, data exports, financial reports, valuation examples, and industry comparison guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Tushare API token, which could be exposed if stored in shell profiles, shared logs, or copied into prompts.

Mitigation: Use a secret manager or session-only environment variable for TUSHARE_TOKEN and avoid running the helper where logs are shared.

Risk: Unpinned Python dependencies can introduce supply-chain or reproducibility issues in production environments.

Mitigation: Pin and review dependencies before production use.

Risk: Scheduled Feishu jobs can distribute financial data or generated reports automatically.

Mitigation: Review each scheduled job, destination, and prompt before enabling automated delivery.

Risk: Market and financial data may be delayed, incomplete, or unsuitable as standalone investment advice.

Mitigation: Review source data, assumptions, and generated analysis before using outputs in investment or reporting decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangzhaofeng-max/skills/tushare-finance-pro)
- [Tushare Pro](https://tushare.pro)
- [Tushare Pro API documentation](https://tushare.pro/document/2)
- [Bundled API reference index](artifact/reference/README.md)
- [Quick reference](artifact/QUICK_REFERENCE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; helper code may return pandas DataFrames, dictionaries, CSV, or Excel outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Tushare Pro token and Python dependencies; financial data outputs should be reviewed before use in investment or reporting decisions.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
