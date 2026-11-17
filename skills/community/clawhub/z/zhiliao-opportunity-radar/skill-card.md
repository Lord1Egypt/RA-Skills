## Description:

按行业、产品和地区扫描拟建项目、采购意向及临期续约机会，并生成按价值排序的商机清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

销售、商务拓展和采购市场研究人员可按行业、产品及地区寻找尚未招标的项目线索，查看机会排序、公开数据出处和建议的后续动作。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vendor searches can consume paid account credits.

Mitigation: Check the estimated credit cost before scanning and request approval before exceeding the planned query budget.

Risk: Automatic account registration sends platform, CPU architecture and a hashed MAC-derived device value to the vendor.

Mitigation: Prefer an existing ZLBX_API_KEY; obtain explicit consent before registration, or decline it to avoid sending device-derived data.

Risk: The skill stores an API key locally and writes shareable reports to the home directory.

Mitigation: Protect the local credential file and review report contents before sharing or retaining them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhiliaobiaoxun/skills/zhiliao-opportunity-radar)
- [知了标讯 Skill 文档](https://ai.zhiliaobiaoxun.com/docs/skill)
- [商机雷达工作流](artifact/references/workflow.md)
- [商机雷达清单模板](artifact/references/report-template.md)

## Skill Output:

**Output Type(s):** [Markdown, HTML report, Guidance]

**Output Format:** [Markdown opportunity list with an optional or full-scan HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranked opportunities include source links, scan scope, data gaps and suggested next steps; full scans save a shareable HTML report locally.]

## Skill Version(s):

1.0.6 (source: skill frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
