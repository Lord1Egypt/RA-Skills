## Description:

Russian-language customer support automation skill for categorizing tickets, tracking SLA risk, routing escalations, drafting customer replies, preparing CRM-oriented customer summaries, and producing NPS/CSAT and onboarding reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raaipro](https://clawhub.ai/user/raaipro)

### License/Terms of Use:

MIT-0

## Use Case:

Support leaders, COOs, CEOs, and support teams use this skill to standardize Russian-language helpdesk operations for businesses with recurring ticket volume. It helps classify tickets, monitor SLA status, route escalations, draft customer replies, and prepare operational reports.

### Deployment Geography for Use:

Global; content and defaults are oriented to Russian-language support operations.

## Known Risks and Mitigations:

Risk: The skill asks for broad model-provider and integration credentials for support, CRM, Telegram, and analytics workflows.

Mitigation: Use least-privilege, integration-specific credentials only after enabling the corresponding integration, and keep provider keys outside skill text and shared artifacts.

Risk: The skill describes automated customer replies, CRM updates, escalation routing, and refund-related actions.

Mitigation: Require human approval for externally sent replies, refunds, compensation, and high-impact CRM changes, especially for legal threats, VIP customers, or large refund amounts.

Risk: Customer messages, CRM history, LTV, and support metrics may contain sensitive personal or business data.

Mitigation: Define privacy, retention, and access-control rules before connecting production CRM or support-channel data.

Risk: Ticket categorization, sentiment scores, SLA reports, and NPS/CSAT analysis depend on clean support data and named escalation owners.

Mitigation: Validate categories, SLA settings, L2/L3 owners, and reports during rollout; treat outputs as operational recommendations until reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raaipro/skills/raai-price-probe-dogovornaya-20260421)
- [README](artifact/README.md)
- [Onboarding guide](artifact/docs/onboarding.md)
- [Anti-fail guide](artifact/docs/anti-fail.md)
- [Quick start examples](artifact/examples/quick-start.md)
- [Configuration template](artifact/config.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with structured tables, checklists, code/config snippets, shell commands, and operational support reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Russian-language defaults; optional CRM, Telegram, and analytics integrations require user-provided credentials.]

## Skill Version(s):

0.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
