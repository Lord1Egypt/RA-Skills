## Description:

Automates Russian-language customer support workflows for ticket categorization, SLA tracking, escalation routing, sentiment-aware responses, CRM context, reports, and operator onboarding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raaipro](https://clawhub.ai/user/raaipro)

### License/Terms of Use:

MIT-0

## Use Case:

Support leaders, operators, and implementation teams use this skill to standardize customer support intake, prioritize tickets, monitor SLA risk, draft responses, route escalations, and produce operational reports for SaaS, e-commerce, marketplace, and service businesses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad customer-support automation may affect refunds, CRM updates, ticket closure, and outbound customer messages.

Mitigation: Require human approval for refunds, CRM writes, ticket closure, and outbound messages until the workflow is reviewed and narrowed.

Risk: The skill handles customer data and optional CRM, Telegram, Sheets, and API credentials.

Mitigation: Define privacy and retention rules before deployment, and do not add live credentials until access controls and data handling are approved.

Risk: Server security evidence reports broad triggers and broken installation/build scripts.

Mitigation: Narrow triggers, fix or replace install/build scripts, and rerun smoke testing before installing in a real support environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raaipro/skills/raai-price-probe-zero-20260421)
- [README](artifact/README.md)
- [Quick start examples](artifact/examples/quick-start.md)
- [Onboarding guide](artifact/docs/onboarding.md)
- [Anti-fail guide](artifact/docs/anti-fail.md)
- [ROI guide](artifact/docs/roi.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured text with tables, checklists, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Russian-language operational outputs; quality depends on configured SLA, escalation owners, ticket categories, and CRM/customer data.]

## Skill Version(s):

0.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
