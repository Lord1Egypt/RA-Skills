## Description:

交付 Excel 前查公式错误、隐藏行列与外部引用

This skill is ready for commercial/non-commercial use.

## Publisher:

[cxdanger123-commits](https://clawhub.ai/user/cxdanger123-commits)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要在发送、共享或导入前检查 Excel 文件的用户，识别公式错误、外部引用、文本型数字、隐藏内容及文件结构异常，并指出需要人工确认的业务口径。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script reads cached formula results and does not recalculate formulas, so cached values may be empty or stale.

Mitigation: Open and save the workbook in Excel or WPS before relying on cached formula results, and have a person confirm business definitions the structural checks cannot assess.

## Reference(s):

- [ClawHub release: excel表格质检 (1.0.0)](https://clawhub.ai/cxdanger123-commits/skills/xlsx-qc)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON]

**Output Format:** [Chinese text or Markdown report; JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports structural checks and cached formula values; does not recalculate formulas.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
