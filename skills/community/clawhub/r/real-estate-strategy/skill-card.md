## Description:

地产项目前期产策定位技能，用于新项目立项研判、竞品分析报告、产品定位方案、投前风险排查和客户研究报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[luojiangyong](https://clawhub.ai/user/luojiangyong)

### License/Terms of Use:

MIT-0

## Use Case:

Real-estate development, investment, and strategy teams use this skill to draft early-stage project positioning work, including land assessment, competitor analysis, customer research, product recommendations, and pre-investment risk checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project names, internal deal context, or site details may be sent to external search providers during web-search-assisted research.

Mitigation: Avoid confidential identifiers in searches unless approved, and use sanitized or generalized project context when external search is not appropriate.

Risk: The bundled report script writes generated files to a hard-coded local path and has unresolved filename sanitization and HTML escaping concerns.

Mitigation: Review and fix the output directory, filename sanitization, and HTML escaping before running the script in a sensitive business environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luojiangyong/skills/real-estate-strategy)
- [产策方案撰写框架](artifact/references/工作机制.md)
- [产品定位四要素](artifact/references/产品定位方法.md)
- [投前产策两大重点](artifact/references/投前产策要点.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports, text guidance, generated report files, and optional HTML, Word, PPT, or PDF output guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request project name, city or district, planning indicators, site context, market data, and preferred output format.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
