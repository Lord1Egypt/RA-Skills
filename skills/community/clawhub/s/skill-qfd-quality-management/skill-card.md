## Description:

将客户需求转化为产品设计规范和质量目标的质量管理工具；当用户需要构建质量屋(VOC分析)、评估需求优先级或计算技术权重时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality managers, product teams, and developers use this skill to structure customer voices, build House of Quality matrices, and calculate technical priority weights for product quality planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated matrices, relationship strengths, and priority rankings can be misleading if treated as final business decisions.

Mitigation: Have domain experts review relationship values, technical targets, and rankings before using the outputs for product or quality decisions.

Risk: Poor-quality or misplaced JSON/CSV inputs can lead to unreliable analysis outputs.

Mitigation: Keep input and output paths in a dedicated workspace and validate VOC, history, and matrix data before running the scripts.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-qfd-quality-management)
- [ClawHub skill listing](https://clawhub.ai/duding-engicool/skills/skill-qfd-quality-management)
- [House of Quality template and data specification](references/hoq_template.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, code]

**Output Format:** [Markdown guidance with JSON schemas and Python command examples; scripts can emit JSON or Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local Python scripts over project-local JSON/CSV files; generated matrices and rankings require review before business decisions.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
