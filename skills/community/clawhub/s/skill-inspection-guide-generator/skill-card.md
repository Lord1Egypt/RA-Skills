## Description:

根据产品技术文件自动生成检验指导书，支持多种格式技术文件解析、Excel 和 Word 模板定制，并将关键信息组织为标准化检验指导书。

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality engineers, supplier quality teams, and operations staff use this skill to turn product technical documents into inspection instructions, quality inspection standards, or supplier inspection requirements. It helps the agent ask for template preferences, structure inspection data, and generate a standardized Excel workbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports unsafe workbook output handling in the local Excel-generation script.

Mitigation: Use trusted technical documents and templates, choose a controlled output directory, and review generated workbook cells before sharing.

Risk: Product names or extracted values may be unsafe if they begin with spreadsheet formula characters or contain path separators.

Mitigation: Avoid those inputs until the script is hardened, or sanitize them before generating a workbook.

Risk: Generated inspection standards can be incomplete when the source technical files do not specify a requirement.

Mitigation: Keep unclear standards marked as "需确认" and require user review before the guidance is used operationally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-inspection-guide-generator)
- [Publisher profile](https://clawhub.ai/user/duding-engicool)
- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-inspection-guide-generator)
- [Inspection guide format](references/inspection_guide_format.md)
- [Template requirements](references/template_requirements.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JSON inspection data and generated Excel workbook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workbooks are named with the product name and current date; unclear inspection standards are marked for confirmation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
