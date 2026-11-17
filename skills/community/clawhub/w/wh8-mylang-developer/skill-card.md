## Description:

Helps agents produce WT8 Mai-language quantitative trading model code, backtesting guidance, parameter optimization advice, strategy execution notes, and position risk management guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kun-wang-0717](https://clawhub.ai/user/kun-wang-0717)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-system users use this skill to draft and review WT8 Mai-language strategy models, classify requests, reference supported functions, and prepare backtests, optimization workflows, simulated runs, and risk-control logic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated strategies can include order-capable WT8 trading logic that may be used in live environments without sufficient confirmation.

Mitigation: Treat all generated strategies as drafts, verify simulation versus live mode, and require explicit human approval before any order-capable deployment.

Risk: Backtest results may not reflect real execution conditions such as slippage, liquidity, symbol selection, position sizing, drawdowns, or stop behavior.

Mitigation: Validate symbols, sizing, slippage assumptions, liquidity, drawdown limits, and stop behavior with backtesting and paper trading before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kun-wang-0717/skills/wh8-mylang-developer)
- [WT8 Mai-language tutorial](https://wt8.wenhua.com.cn/#/download/download/2)
- [Wenhua syntax guide](https://www.wenhua.com.cn/guide/views41a3.htm)
- [Wenhua operator syntax guide](https://www.wenhua.com.cn/guide/views41a.htm)
- [Wenhua signal filtering details](https://www.wenhua.com.cn/popwin/guolvmx3.htm)
- [Artifact README](artifact/README.md)
- [Function index](artifact/FUNCTIONS/INDEX.md)
- [Common mistakes and edge cases](artifact/EDGE_CASES/common_mistakes.md)
- [Model templates](artifact/TEMPLATES/model_template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with WT8 Mai-language code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include trading-model drafts, backtest and optimization instructions, execution notes, and risk-management checks.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact/skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
