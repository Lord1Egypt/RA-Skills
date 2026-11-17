## Description:

Ai Support Pro is a customer-support automation skill for classifying tickets, tracking SLA, routing L1/L2/L3 escalations, analyzing sentiment, drafting replies, onboarding support agents, and producing NPS/CSAT reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raaipro](https://clawhub.ai/user/raaipro)

### License/Terms of Use:

MIT-0

## Use Case:

Support leaders, COOs, CEOs, and customer-support teams use the skill to standardize intake, prioritization, SLA monitoring, escalation, response drafting, reporting, and agent onboarding for businesses handling recurring support tickets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive customer data and propose CRM or ticket actions.

Mitigation: Start with test tickets, connect real channels only after privacy controls are defined, and require administrator approval for CRM write actions.

Risk: Credentials for AI providers, messaging channels, and CRM systems may be mishandled during setup.

Mitigation: Keep real API keys out of config files, use environment variables or a secrets manager, and grant least-privilege access.

Risk: Automated routing or response guidance can be wrong for refunds, legal threats, VIP customers, or high-severity incidents.

Mitigation: Require human review for high-priority, financial, legal, VIP, and escalation decisions before messages or actions are finalized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raaipro/skills/raai-ai-support-pro)
- [Quick start](examples/quick-start.md)
- [Onboarding guide](docs/onboarding.md)
- [Limitations and anti-fail guide](docs/anti-fail.md)
- [ROI guide](docs/roi.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured ticket summaries, SLA reports, escalation handoffs, response drafts, onboarding checklists, and setup commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configuration of company details, support-team roles, SLA rules, escalation contacts, and optional CRM or channel credentials before live use.]

## Skill Version(s):

3.5.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
