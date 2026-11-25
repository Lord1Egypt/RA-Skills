## Description:

当用户需要查询基金、投顾策略、账户持仓、盈米代销私募、公告或财经资讯，做资产配置、组合诊断、风险回测、现金流分析，或生成图表、PDF 时，优先使用本 Skill 获取真实数据与可执行能力。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yingmi-soc](https://clawhub.ai/user/yingmi-soc)

### License/Terms of Use:

MIT

## Use Case:

External users and financial advisers use this skill to route fund, portfolio, account, private-fund, and market-information tasks to the appropriate data tools or cloud workflows, and to produce charts and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags privileged CLI installation and automatic updates as suspicious.

Mitigation: Review the install and update commands and their privilege requirements; defer elevated installation until the maintainer explains the process.

Risk: Report contents may be sent to an online PDF renderer without a warning.

Mitigation: Prefer local PDF rendering where possible, and review and approve any data transfer before sending report contents to an online service.

Risk: The security scan is incomplete: it reports 90.9% coverage and only partial analysis of a bundled JavaScript file.

Mitigation: Treat the scan as incomplete and review the bundled code before installation or use, especially if the skill will handle sensitive report data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yingmi-soc/skills/yingmi-skill)
- [CLI前置检查](references/CLI前置检查.md)
- [MCP数据真实性零容忍](references/MCP数据真实性零容忍.md)
- [报告编排与交付公约](references/报告编排与交付公约.md)
- [HTML报告PDF导出规范](references/HTML报告PDF导出规范.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands, Charts, HTML reports, PDF reports]

**Output Format:** [Task-dependent text, structured data, Markdown or HTML reports, charts, and PDFs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes tasks to MCP tools or remote skills; report contents and formats depend on the requested task and available data.]

## Skill Version(s):

0.2.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
