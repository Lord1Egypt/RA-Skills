## Description:

交易日开盘前（8:00-9:25）生成A股市场全景简报，整合市场结构、资金热度、风格轮动、板块强弱等信息，帮助把握当日投资主线。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksky521](https://clawhub.ai/user/ksky521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill before the A-share trading session to collect DaxiAPI market data and produce a structured Markdown premarket briefing. It supports market overview, investment-theme identification, and risk review, but is not intended for non-trading days, intraday real-time analysis, or deep single-stock research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to run daxiapi-cli with the @latest package tag, which can execute a different remote CLI version over time.

Mitigation: Review before installing and use a vetted, pinned daxiapi-cli version for operational use.

Risk: The skill requires a DaxiAPI token and includes workflows that can expose token values through terminal commands or agent logs.

Mitigation: Store the token securely, use least-privilege access, avoid printing token values, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ksky521/skills/xiapi-premarket-briefing)
- [DaxiAPI](https://daxiapi.com)
- [CLI 命令参考](references/cli-commands.md)
- [Token 配置指南](references/token-setup.md)
- [字段说明和名词解释](references/field-descriptions.md)
- [API 参考文档](references/api-reference.md)
- [盘前简报示例输出](assets/example-output.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Structured Markdown report with inline shell commands and market-data guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a dated six-section A-share premarket briefing with numerical support and an investment-risk disclaimer.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
