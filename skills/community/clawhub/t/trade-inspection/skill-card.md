## Description:

帮助外贸出口商解读检测报告、审核发票、箱单、提单和产地证一致性，初步核查HS编码和出口合规要求，并生成验货报告与合规说明函草稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lzh1998-ui](https://clawhub.ai/user/lzh1998-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Exporters, manufacturers, and trade operations teams use this skill to prepare and review export inspection, customs, certification, and shipment documentation before human compliance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product search terms may be sent to a placeholder external HS lookup API if online lookup is enabled.

Mitigation: Keep HS lookup offline unless an external service is intentionally configured and approved for the data being processed.

Risk: Generated HS classifications, export-control screening, certification checks, and compliance letters may be incomplete or incorrect.

Mitigation: Treat outputs as drafts for initial screening and route final decisions to qualified customs, compliance, or legal reviewers.

Risk: Trade documents can contain confidential product, supplier, customer, and shipment data.

Mitigation: Review the skill before installation and avoid processing sensitive records in environments that are not approved for that data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lzh1998-ui/skills/trade-inspection)
- [主流出口市场检测标准对照表](references/standards.md)
- [单证审核逐项清单](references/document_checklist.md)
- [常见出口品类 HS 编码参考与风险提示](references/hs_codes.md)
- [主要出口目的国禁限运清单摘要](references/export_restrictions.md)
- [英文合规说明函可填充模板](references/compliance_letters.md)
- [出口验货报告模板](assets/inspection_report_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports, checklists, risk matrices, compliance letter drafts, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory drafts and should be reviewed by qualified customs, compliance, or legal professionals before use.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
