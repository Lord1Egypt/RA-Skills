## Description:

解析微信群接龙文本，提取商品清单和订单明细，生成按人透视表，并在腾讯文档连接器可用时导出明细和汇总表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingguotu](https://clawhub.ai/user/dingguotu)

### License/Terms of Use:

MIT-0

## Use Case:

People managing WeChat group-buy orders use this skill to turn pasted jielong messages into participant-level order tables, totals, and optional Tencent Docs spreadsheets for review and sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Group-order text can include participant nicknames, room numbers, and order details that may be sensitive when exported to Tencent Docs.

Mitigation: Confirm the group is comfortable with Tencent Docs export; for sensitive groups, keep output local or remove room numbers before export.

Risk: Abbreviated product names, typos, and ambiguous matches can lead to incorrect order allocation or totals.

Mitigation: Review marked ambiguous matches, typo corrections, and totals against the original jielong message before relying on the table.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingguotu/skills/wechat-jielong-parser)
- [Publisher profile](https://clawhub.ai/user/dingguotu)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown tables and Tencent Docs spreadsheet content when the connector is available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a Tencent Docs link, product/order summaries, total amounts, and notes about closed items or ambiguous matches.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
