## Description:

面向 A 股个人投资者，提供盘前分析、选股、持仓与风险检查、交易计划和盘后复盘的研究辅助。

This skill is for research and development only.

## Publisher:

[yjkj999999](https://clawhub.ai/user/yjkj999999)

### License/Terms of Use:

MIT-0

## Use Case:

面向 A 股个人投资者，用于市场与个股研究、组合和风险检查、交易计划及复盘，并生成分析和候选行动建议。内容仅作学习与研究参考；交易前应核验信息并由用户确认。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with high confidence because reported trading instructions may exceed its stated research and manual-confirmation scope.

Mitigation: Review the order-related workflow carefully, treat outputs as research material, and verify and manually confirm any proposed trade before acting.

Risk: ClawScan reports installation guidance that could run unpinned or remotely fetched code; it places the release in Review and recommends DO_NOT_INSTALL.

Mitigation: Follow the scan guidance and review the installation steps and fetched code before considering installation; limit tools and permissions to those intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yjkj999999/skills/super-stock-trading)
- [ClawHub publisher profile](https://clawhub.ai/user/yjkj999999)
- [Daily workflow](references/daily_workflow.md)
- [Risk rules](references/risk_rules.md)
- [Short-line trading reference](references/short_line_mastery.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Configuration]

**Output Format:** [Chinese-language market and portfolio analysis, checklists, and plans in Markdown; JSON configuration or portfolio/watchlist files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research support for user review; verify current information and confirm any trading decision manually.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
