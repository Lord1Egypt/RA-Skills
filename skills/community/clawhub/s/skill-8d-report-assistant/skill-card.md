## Description:

8D问题解决报告生成工具，采用分步引导和对话式信息收集模式，生成结构化详细报告，适用于汽车等行业质量问题分析场景，覆盖D1-D8八大步骤。

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality engineers, manufacturing teams, and external ClawHub users can use this skill to collect 8D problem-solving information step by step, guide 5M1E and 5WHY analysis, and produce a structured Chinese-language 8D report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 8D reports may contain personal contact details, customer information, product identifiers, and quality data.

Mitigation: Review and redact sensitive fields before sharing or exporting a Word report.

Risk: Generated root-cause analysis can be incomplete or misleading when the user provides sparse or unverified information.

Mitigation: Have a qualified quality owner review the D4 analysis, supporting data, corrective actions, and closure criteria before operational use.

## Reference(s):

- [8D Methodology and Scoring Standard](artifact/references/8d-methodology.md)
- [Dialogue Guide and Best Practices](artifact/references/dialogue-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/duding-engicool/skills/skill-8d-report-assistant)
- [Server-Resolved Source Repository](https://github.com/duding-engicool/skill-8d-report-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Chinese-language Markdown report with optional Word document export after user confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides users through D0-D8 information collection and asks for confirmation before Word export.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
