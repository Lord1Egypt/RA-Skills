## Description:

基于 Brent Penfold《交易圣经》框架，为股票交易生成完整的交易预案（Setup）和交易计划（Plan）。当用户询问「帮我制定交易计划」、「帮我做交易预案」、「XX股票怎么买」、「帮我规划一下XX股票的入场和止损」时使用此技能。触发前提：用户明确指定了具体股票代码或名称。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thatshinji](https://clawhub.ai/user/thatshinji)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading-focused agents use this skill to prepare structured stock trading setups and plans for a specified stock code or name. It gathers market, news, and fundamental data, then formats technical analysis, entry, stop-loss, target, position-sizing, and pre-trade checklist guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce concrete trading instructions, including buy, sell, stop-loss, target-price, and position-size guidance.

Mitigation: Require human review before any real trade and present outputs as planning support, not personalized financial advice.

Risk: The skill does not clearly require suitability inputs before making recommendations.

Mitigation: Collect and review user-specific risk tolerance, account constraints, jurisdiction, and investment objectives before relying on generated plans.

Risk: Market, news, and fundamentals data may be stale, incomplete, or unavailable.

Mitigation: Verify quotes, news, fundamentals, and order parameters against trusted market data and brokerage systems before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thatshinji/skills/trading-plan-generator)
- [交易预案框架](references/交易预案.md)
- [交易计划框架](references/交易计划.md)
- [Brent Penfold framework notes](references/penfold-framework.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with tables, checklists, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include specific buy, sell, stop-loss, target-price, and position-size guidance for a named stock.]

## Skill Version(s):

1.2.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
