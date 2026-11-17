## Description:

一人公司商务助手 — 从获客到收款的文档生成+策略建议+项目管理。帮你高效完成商务全流程，覆盖提案、合同、报价、催款等15+文档类型。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiu-difeng](https://clawhub.ai/user/qiu-difeng)

### License/Terms of Use:

MIT-0

## Use Case:

Solo operators and small-business agents use this skill to generate China-market business documents, negotiation guidance, client records, project tracking summaries, collection reminders, and operating reviews from local JSON data.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill can store real customer, contract, project, and payment information in local JSON files.

Mitigation: Use a dedicated workspace and keep data/ out of source control and cloud sync unless that sharing is intended.

Risk: The skill can persist and automatically change client, project, and payment records.

Mitigation: Confirm every proposed write to clients.json or deals.json before accepting the change.

Risk: Installing with a moving @latest package can change installer behavior over time.

Mitigation: Pin or verify the installer version before installation.

Risk: Generated contracts, tax language, and collection guidance are jurisdiction-specific business aids and may be unsuitable for high-value or unusual matters.

Mitigation: Review important documents with a qualified legal or tax professional before use.

## Reference(s):

- [Solo Forge ClawHub release page](https://clawhub.ai/qiu-difeng/skills/solo-forge)
- [README](README.md)
- [Proposal and Lead Generation Module](references/proposal.md)
- [Proposal Templates](references/proposal-templates.md)
- [Contract and Legal Module](references/contract.md)
- [Contract Templates](references/contract-templates.md)
- [Quotation and Collections Module](references/quotation.md)
- [Quotation Templates](references/quotation-templates.md)
- [Negotiation Decision Tree](references/negotiation.md)
- [Project Tracking Module](references/tracking.md)
- [Client Management Module](references/clients.md)
- [Business Review Module](references/business-review.md)
- [Business Review Templates](references/review-templates.md)
- [Delivery Management Module](references/delivery.md)
- [Delivery Templates](references/delivery-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration, Files]

**Output Format:** [Markdown business documents, strategy guidance, and JSON record updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local JSON files under data/ for client, project, payment, and configuration records.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
