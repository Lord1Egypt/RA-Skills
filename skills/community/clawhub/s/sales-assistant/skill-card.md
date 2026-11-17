## Description:

销售助手（Sales Assistant）协助销售团队整理客户商机、生成客户画像和拜访纪要、提炼需求、建议跟进动作、提示商务风险并维护客户档案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[afeicn](https://clawhub.ai/user/afeicn)

### License/Terms of Use:

MIT-0

## Use Case:

Sales representatives, sales operations staff, presales staff, and sales managers use this skill to turn Feishu messages, customer records, meeting notes, and demand materials into structured sales drafts, risk notes, follow-up actions, human-review items, and archive records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive sales, customer, contract, employee, financial, and technical information.

Mitigation: Deploy only after Feishu access control, authorization checks, masking, audit logging, retention, and deletion procedures are configured.

Risk: Draft sales recommendations could be mistaken for final pricing, delivery, contract, or external communication decisions.

Mitigation: Route pricing positions, business commitments, delivery timelines, sensitive customer information, and externally sent materials to human approval before use.

Risk: CRM or archive records can preserve unsupported assumptions if source material is incomplete.

Mitigation: Require source-grounded outputs, mark missing information as needing confirmation, and keep input, output, reviewer, and archive-location audit records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afeicn/skills/sales-assistant)
- [README](artifact/README.md)
- [Workflows](artifact/workflows.md)
- [Runbook](artifact/runbook.md)
- [Sales skills catalog](artifact/skills/sales_skills.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and structured text templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces sales summaries, opportunity cards, customer profiles, meeting notes, need summaries, follow-up plans, risk lists, human-review notes, and archive records.]

## Skill Version(s):

0.1.0 (source: server release metadata and employee.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
