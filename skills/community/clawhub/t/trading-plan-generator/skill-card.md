## Description: <br>
基于 Brent Penfold《交易圣经》框架，为股票交易生成完整的交易预案（Setup）和交易计划（Plan）。当用户询问「帮我制定交易计划」、「帮我做交易预案」、「XX股票怎么买」、「帮我规划一下XX股票的入场和止损」时使用此技能。触发前提：用户明确指定了具体股票代码或名称 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thatshinji](https://clawhub.ai/user/thatshinji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading-focused agents use this skill to prepare structured stock trading setups and plans for a specified A-share, Hong Kong, or U.S. stock. The skill guides market data review, news review, fundamental checks, technical analysis, position sizing, stop-loss planning, and a pre-trade checklist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce actionable stock trading guidance that may be unsuitable for a user's financial situation. <br>
Mitigation: Treat outputs as research rather than personalized financial advice, and make independent decisions before risking capital. <br>
Risk: Trading plans may be wrong if market, news, or fundamental data is stale or incomplete. <br>
Mitigation: Verify market data and review the referenced Longbridge and WenCai tool outputs before acting. <br>
Risk: The skill includes shell commands for data collection tools that may not be installed or may have their own trust requirements. <br>
Mitigation: Confirm the Longbridge and WenCai tools are available and trusted in the execution environment before running the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thatshinji/trading-plan-generator) <br>
- [Publisher profile](https://clawhub.ai/user/thatshinji) <br>
- [Penfold framework reference](references/penfold-framework.md) <br>
- [Trading plan reference](references/交易计划.md) <br>
- [Trading setup reference](references/交易预案.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with tables, checklists, calculations, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a stock-specific trading setup and plan after market, news, fundamental, and technical review.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
