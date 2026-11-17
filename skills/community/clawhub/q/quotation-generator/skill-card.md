## Description:

报价单生成可根据用户上传的物料价格表和 Excel 报价模板，分析模板结构、匹配产品价格、计算总价，并生成填充完成的报价单 Excel 文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaolongcai](https://clawhub.ai/user/shaolongcai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business teams use this skill to turn uploaded price lists and Excel quotation templates into completed customer quotation workbooks. It is useful when product pricing, model selection, template column mapping, formula preservation, and customer fields must be handled consistently.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spreadsheet formula injection can occur if user-controlled text from product names, customer fields, or uploaded price lists is written directly into Excel cells.

Mitigation: Treat all user and price-list text as untrusted, write text fields as literal strings, and permit formulas only in trusted template-controlled cells.

Risk: Incorrect model matching or ambiguous product selection can produce inaccurate customer quotations.

Mitigation: Require clarification when a product has multiple models, do not invent missing products, and review product, quantity, price, and total fields before sending generated files externally.

## Reference(s):

- [报价数据规范](references/data-schema.md)

## Skill Output:

**Output Type(s):** [files, text, configuration, guidance]

**Output Format:** [Excel workbook with Markdown or JSON-style operational summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workbooks are based on user-supplied price lists and Excel templates; product text, pricing, model selection, and formulas should be reviewed before customer use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
