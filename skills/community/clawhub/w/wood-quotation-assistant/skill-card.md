## Description: <br>
木工厂报价助手用于从图纸和文字描述中提取尺寸与工艺信息，匹配材料阶梯价格、损耗率和利润率，并生成木作报价明细与 Excel 报价单。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gh488](https://clawhub.ai/user/gh488) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Woodworking shops, furniture manufacturers, display-case makers, and custom millwork vendors use this skill to estimate material costs, process costs, loss, total cost, and quote price from drawings or supplied dimensions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default pricing, loss-rate, profit-margin, branding, and contact details may not match the deploying business. <br>
Mitigation: Review and customize those values before using the skill for operational quotations. <br>
Risk: Internal pricing mode can expose real purchase data if enabled in an untrusted workspace. <br>
Mitigation: Use internal pricing mode only in a trusted workspace; use public or example configuration for external workflows. <br>
Risk: Broad trigger words may activate the skill for a quotation request that was not intended for this workflow. <br>
Mitigation: Confirm the intended drawing, dimensions, and quotation task before relying on the generated quote. <br>
Risk: Quotation spreadsheets can be exported from the wrong drawing or to an unintended output file. <br>
Mitigation: Confirm the drawing input and output path before exporting Excel quotation workbooks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gh488/wood-quotation-assistant) <br>
- [材料编码对照表](artifact/references/material_codes.md) <br>
- [木工厂报价核算逻辑说明](artifact/references/quotation_logic.md) <br>
- [采购数据配置说明](artifact/data/purchase_cost_data.md) <br>
- [核算模板说明](artifact/data/wood_quotation_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, configuration] <br>
**Output Format:** [Markdown quotation table and optional Excel .xlsx quotation workbook] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Excel export uses openpyxl; PDF drawing parsing uses pdfplumber when installed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
