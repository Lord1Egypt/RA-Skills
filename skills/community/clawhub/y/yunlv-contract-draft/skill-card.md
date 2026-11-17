## Description:

Drafts and reviews foreign trade contracts, sales agreements, Proforma Invoices, Sales Contracts, MOUs, NDAs, and related clauses for payment, delivery, and risk allocation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External trade teams and business users use this skill to draft bilingual international trade contract documents and review contract clauses for payment, delivery, Incoterms, and risk allocation issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential contract drafts and commercial details may be sent to the Yunlv TradeGPT API.

Mitigation: Install only if this external API use is acceptable, and redact bank account details, personal data, and unnecessary confidential terms before use.

Risk: Generated contracts and clause reviews may be incomplete or legally incorrect.

Mitigation: Treat outputs as drafts and obtain qualified legal review before signing or relying on them for regulated, high-value, or complex transactions.

Risk: The skill depends on a bearer token in TRADEGPT_API_KEY.

Mitigation: Scope access to the minimum needed, avoid exposing the key in prompts or logs, and rotate it if disclosure is suspected.

## Reference(s):

- [Yunlv AI homepage](https://yunlvai.com)
- [Yunlv TradeGPT API](https://api.yunlvai.com)
- [Contract Type Templates](references/contract_type_templates.md)
- [Clause Risk Checklist](references/clause_risk_checklist.md)
- [International Commercial Law](references/international_commercial_law.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown contract drafts and review guidance, with JSON risk reports from the included analyzer script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the Yunlv TradeGPT API with TRADEGPT_API_KEY and may generate draft contract text, clause reviews, negotiation priorities, and risk scores.]

## Skill Version(s):

1.1.0 (source: server release and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
