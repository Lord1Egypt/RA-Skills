## Description:

Build a pre-written response library for common customer service inquiries, complaints, and order issues that maintains tone and reduces resolution time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Customer support teams and ecommerce operators use this skill to create reusable support-script libraries for Shopify, TikTok Shop, and Shopee workflows. It helps agents draft policy-aware replies, scenario variants, escalation notes, and maintenance checklists for common customer issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Support scripts could conflict with refund authority, safety-claim escalation, marketplace rules, or internal policy.

Mitigation: Confirm refund limits, safety-claim escalation, marketplace rules, and trigger definitions with the business owner or compliance reviewer before loading scripts into helpdesk macros or auto-replies.

Risk: Placeholders or stale order facts could be sent unchanged or incorrect in customer replies.

Mitigation: Use the quality checklist to verify all placeholders, order-specific details, timeframes, and amounts before scripts are approved or sent.

Risk: Localized scripts may use the wrong tone, formatting, or politeness level for a market.

Mitigation: Have a native speaker review localized script sets and verify dates, currencies, name order, honorifics, and placeholder preservation.

## Reference(s):

- [Support Scripts skill page](https://clawhub.ai/leooooooow/skills/support-scripts)
- [Output Template](references/output-template.md)
- [Scenario Library](references/scenario-library.md)
- [Tone and Policy Guide](references/tone-and-policy-guide.md)
- [Quality Checklist](assets/quality-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown support-script templates, scenario guidance, policy notes, and checklist items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses placeholders such as {{customer_name}}, {{order_id}}, {{tracking_link}}, {{amount}}, and {{eta_date}} for agent customization.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
