## Description:

整理商家提供的至多100行商品名称、颜色、尺寸和型号资料，输出统一命名表、重复与缺失规格报告及含待确认原因的CSV导入草稿；保留原字段和行顺序，重复组所有行均需确认，缺少关键值时先请求补齐，不读取店铺后台。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

外部用户（包括中文小店经营者、小说作者和自媒体创作者）可用它整理自己提供的商品资料，生成统一命名建议、问题报告和可复核的 CSV 导入草稿。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product records may include information the user did not intend to share with the agent.

Mitigation: Share only product records intended for the agent to process.

Risk: A draft CSV may contain unresolved or incorrect product details if imported without review.

Mitigation: Review the CSV and resolve every flagged item before importing it.

Risk: The documented npx installation command may install an unreviewed source or release.

Mitigation: Verify the source and prefer reviewed installer versions and source revisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xxjrq/skills/shop-sku-normalizer-cn)
- [ERPNext project (usage reference only)](https://github.com/frappe/erpnext)
- [ERPNext README (usage reference only)](https://github.com/frappe/erpnext/blob/develop/README.md)

## Skill Output:

**Output Type(s):** [Markdown, CSV text, Guidance]

**Output Format:** [Markdown tables and prose, plus a CSV draft when required product fields are present]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes up to 100 user-provided rows; preserves original values and row order; flags duplicates, missing fields, and items needing confirmation.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
