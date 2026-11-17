## Description:

量化策略助手将自然语言策略需求转化为策略代码，提交回测，支持参数优化，并可在用户请求后进入 QMT 模拟或实盘流程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[listolany](https://clawhub.ai/user/listolany)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative trading users use this skill to turn Chinese natural-language strategy ideas into generated strategy code, run backtests, review results, and optionally prepare parameter optimization or QMT trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate and run trading strategy code.

Mitigation: Review generated strategy code and backtest assumptions before execution.

Risk: The skill can expose a monitoring service during backtests.

Mitigation: Bind the monitor to localhost or protect it with authentication before exposing it beyond a trusted environment.

Risk: The skill can start QMT simulated or live trading workflows.

Mitigation: Require manual confirmation before any QMT trade or probe order and use the workflow only with an intended account.

Risk: The workflow may use QGData credentials or fall back to shared tokens.

Mitigation: Use a disposable or scoped QGData token and avoid relying on global .env files.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/listolany/skills/quant-strategy-assistant)
- [QuantClaw configuration guide](https://gitee.com/GuojinQuant/quant-claw#第四步配置环境变量)
- [qgdata data capability reference](qgdata-reference.md)
- [qgdata SDK user API](references/SDK_USER_API.md)
- [qgdata stock minutes API](references/SDK_USER_API_STK_MINS.md)
- [vnpy_qmt README](QMT-TradingClaw/vnpy_qmt/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, generated Python strategy code, and JSON status summaries from orchestration commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce strategy files, backtest submissions, monitor links, and trading workflow commands depending on user intent.]

## Skill Version(s):

1.0.2 (source: server release metadata, created 2026-04-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
