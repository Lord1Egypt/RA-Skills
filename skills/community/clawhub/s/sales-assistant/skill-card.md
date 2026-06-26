## Description: <br>
销售助手（Sales Assistant）协助销售团队整理商机、分析客户画像、生成拜访纪要、提炼需求、建议跟进动作、提示商务风险并维护客户档案。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afeicn](https://clawhub.ai/user/afeicn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales representatives, commercial staff, presales teams, and sales managers use this skill to turn customer communications, meeting notes, and demand materials into structured opportunity cards, customer profiles, meeting summaries, follow-up plans, risk notes, and CRM archive drafts. Human confirmation is required for pricing, commercial commitments, delivery timelines, sensitive customer information, and outbound materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive customer, sales, meeting, contract, and CRM information. <br>
Mitigation: Deploy only where the team is authorized to process this data; configure permissions, audit logs, archive retention, and prefer redacted or minimized inputs. <br>
Risk: Generated sales guidance could be mistaken for approved pricing, delivery, contract, or outbound commitments. <br>
Mitigation: Require named human approval for pricing language, commercial commitments, delivery timelines, customer-sensitive information, and externally sent materials. <br>
Risk: Incomplete or weak input materials could lead to unsupported opportunity or customer conclusions. <br>
Mitigation: Mark unsupported items as needing human confirmation and request missing materials instead of presenting assumptions as facts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/afeicn/sales-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Structured Markdown and template-based sales records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are drafts, recommendations, checklists, summaries, risk notes, and archive records that require human confirmation for high-impact sales actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence and employee.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
