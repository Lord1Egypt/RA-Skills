## Description:

舟谱系统订单导入模板生成（自提订单+调拨订单分开，每表只有1个sheet）。当下单表数据需要转化为舟谱系统可导入的Excel格式时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyzhangjf](https://clawhub.ai/user/xyzhangjf)

### License/Terms of Use:

MIT-0

## Use Case:

Operations users and agents use this skill to convert Chinese-language Zhoupu order workbooks and price tables into self-pickup and transfer-order Excel import templates. It supports customer name mapping, source document numbering, barcode and unit lookup, quantity checks against workbook total rows, and required-field validation before Zhoupu import.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect quantities, barcodes, units, prices, or self-pickup columns could lead to wrong Zhoupu imports.

Mitigation: Review generated spreadsheets before importing and compare generated totals with the workbook total rows.

Risk: The documentation and generated self-pickup column count do not fully match.

Mitigation: Confirm the generated self-pickup workbook against the current Zhoupu import template before upload.

Risk: Orders may bypass the documented sales-manager review step if the workflow is used mechanically.

Mitigation: Keep the documented review by 郝洋 before generating and importing final Zhoupu templates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xyzhangjf/skills/zhoupu-order-import)
- [Zhoupu portal](https://portal.zhoupudata.com/saas/main)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Excel workbooks with terminal validation messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an order workbook, price workbook, and arrival date; supports optional sheet selection, output path, start sequence, and supplemental prices.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
