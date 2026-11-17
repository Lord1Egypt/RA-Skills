## Description:

Excel数据处理向导，提供数据报表，模板填充，批量处理与图表可视化功能。支持条件格式，数据透视表，格式美化与文件分析。适用于财务报表，销售数据统计，库存管理，月度季度报告等Excel数据场景。涵盖结构识别，数据读取，数据写入，问题诊断等表格操作能力。内置openpyxl引擎，含单元格格式控制，多Sheet操作，数据校验，密码保护。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations teams use this skill to guide Excel workbook analysis, report generation, template filling, batch merging, formatting, formulas, charts, and file troubleshooting with Python-based spreadsheet workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vague API-key and network guidance could lead users to provide credentials that are not needed for local Excel processing.

Mitigation: Do not provide API keys or credentials unless the publisher clarifies a specific optional integration and why it is needed.

Risk: File-changing workflows may overwrite or alter workbooks if generated code is run against original files.

Mitigation: Use only files explicitly provided for the task, save results to new output files, and review generated scripts before execution.

Risk: Excel workbooks can contain sensitive business or personal data.

Mitigation: Avoid logging workbook contents or secrets, and process sensitive files only in an approved local or controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/xlsx-data-wizard-cn)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with Python/openpyxl code blocks, command examples, and Excel workbook output instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify .xlsx workbooks; users should prefer new output files and review generated code before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
