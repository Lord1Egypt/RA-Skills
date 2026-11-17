## Description:

Tushare Pro 金融数据 API 查询助手。用于帮助用户查询中国股票、基金、期货、债券等金融数据。当用户需要获取股票行情、财务数据、基础信息、宏观经济数据时使用此 skill。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ulnacranium17](https://clawhub.ai/user/ulnacranium17)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to get concise guidance for querying Tushare Pro financial data across China stocks, funds, futures, bonds, and macroeconomic datasets. It helps users choose common Tushare interfaces, format security codes, and prepare Python SDK or HTTP API requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill can involve sending a Tushare token and query parameters to Tushare's API.

Mitigation: Use a proper Tushare token, avoid pasting unrelated secrets, and review requests before sending them.

Risk: Tushare account points, rate limits, or frequency limits may be consumed by generated API requests.

Mitigation: Monitor account usage and confirm that high-frequency or point-consuming calls are necessary before running them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ulnacranium17/skills/tushare-openclaw-skill)
- [Tushare Official Website](https://tushare.pro)
- [Tushare API Documentation](https://tushare.pro/document/2)
- [Tushare Points and Frequency Documentation](https://tushare.pro/document/1?doc_id=290)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Tushare API names, stock-code formats, request parameters, and token setup guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
