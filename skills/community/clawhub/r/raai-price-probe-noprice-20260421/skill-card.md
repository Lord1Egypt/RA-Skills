## Description:

Russian-language customer support automation skill for ticket categorization, SLA tracking, escalation workflows, sentiment-aware response drafting, NPS/CSAT reporting, onboarding, and optional CRM integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raaipro](https://clawhub.ai/user/raaipro)

### License/Terms of Use:

MIT-0

## Use Case:

Support leaders, operations teams, and developers use this skill to standardize high-volume customer support workflows: classify incoming tickets, monitor SLA risk, escalate sensitive cases, draft customer replies, generate service-quality reports, and configure CRM/helpdesk handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad customer-data processing across tickets, CRM records, sentiment analysis, and support reports can expose sensitive customer information.

Mitigation: Review before installing in a real support environment, keep live secrets out of config.yaml, and use least-privilege credentials only for explicitly enabled integrations.

Risk: CRM or ticket mutations could update customer records, create tickets, change tags, or alter statuses without enough scoping.

Mitigation: Require human approval for CRM writes and limit triggers to deliberate commands or approved channels.

Risk: Automatic customer replies and refund handling can send incorrect, unauthorized, or policy-inconsistent messages.

Mitigation: Require human approval for outbound customer messages and refund decisions before using the skill in production support workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raaipro/skills/raai-price-probe-noprice-20260421)
- [Publisher profile](https://clawhub.ai/user/raaipro)
- [README](artifact/README.md)
- [Onboarding guide](artifact/docs/onboarding.md)
- [Anti-fail guide](artifact/docs/anti-fail.md)
- [Quick start examples](artifact/examples/quick-start.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, structured text templates, YAML configuration, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Russian-language support operations outputs; optional integration behavior depends on configured credentials and enabled channels.]

## Skill Version(s):

0.0.1 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
