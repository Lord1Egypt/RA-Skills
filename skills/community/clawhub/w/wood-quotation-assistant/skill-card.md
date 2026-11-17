## Description:

木工厂报价助手。自动匹配阶梯价格、计算损耗率、生成报价明细表（工艺成本/损耗/总成本/报价金额）。支持图纸尺寸提取、多格式导出。触发关键词：算报价、图纸报价、工艺核算、生成报价表、木作报价、板材成本核算。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gh488](https://clawhub.ai/user/gh488)

### License/Terms of Use:

MIT-0

## Use Case:

Woodworking shops, furniture manufacturers, custom millwork vendors, and external business users use this skill to parse drawings or descriptions, estimate material and process costs, apply waste and profit assumptions, and generate quotation details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Excel quotations may include fixed third-party branding or contact details that do not match the installing organization.

Mitigation: Remove or configure embedded business identity fields before producing customer-facing quotation files.

Risk: Spreadsheet content may be interpreted as formulas when exported to Excel.

Mitigation: Sanitize cell values before export and review generated workbooks before sharing them externally.

Risk: Cost estimates depend on local material prices, loss rates, process prices, and profit margin settings.

Mitigation: Configure pricing assumptions for the target shop or supplier policy before relying on generated quotes.

## Reference(s):

- [Material Codes](artifact/references/material_codes.md)
- [Quotation Logic](artifact/references/quotation_logic.md)
- [ClawHub Skill Page](https://clawhub.ai/gh488/skills/wood-quotation-assistant)
- [Publisher Profile](https://clawhub.ai/user/gh488)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tables, JSON-like calculation data, Excel workbook files, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May export .xlsx quotation workbooks and depends on user-configured material prices, loss rates, process prices, and profit margin.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
