## Description:

AI 與交易腳本協作技能。AI 每 5 分鐘監控交易訊號，與腳本並存共生：補充腳本遺漏的訊號、修復失敗交易、糾正錯誤交易、主動執行值得跟隨的交易。持續分析腳本問題並改進。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chungvic](https://clawhub.ai/user/chungvic)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to coordinate an AI agent with automated crypto or stock trading scripts, monitor trading signals, review failed or incorrect trades, and improve trading automation workflows. It is intended for live trading workflows only when the operator has explicit controls and risk limits in place.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to help operate live trading workflows and can propose or retry real trades.

Mitigation: Require paper-trading by default and explicit operator confirmation before every live order.

Risk: Autonomous or repeated trades can cause financial loss if signals, markets, accounts, or parameters are wrong.

Mitigation: Restrict use to approved accounts and markets, enforce maximum trade size and daily loss limits, and maintain a manual kill switch.

Risk: Incorrect token, quantity, slippage, gas, or direction parameters can create failed or erroneous trades.

Mitigation: Require pre-trade checks for token address, trade size, slippage, gas, wallet balance, contract status, and trade direction.

## Reference(s):

- [Trading Checklist](references/trading-checklist.md)
- [Failure Analysis Guide](references/failure-analysis.md)
- [ClawHub Skill Release](https://clawhub.ai/chungvic/skills/trading-coagent-vic)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown/text guidance with optional code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce monitoring notes, failure analysis, script updates, and trading workflow recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
