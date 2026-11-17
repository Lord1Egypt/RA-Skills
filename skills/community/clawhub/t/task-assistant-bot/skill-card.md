## Description:

A Chinese-language order-formatting helper that consolidates same-day order details into a fixed customer notice, internal execution requirements, and a table import row when triggered.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lemonjuice0](https://clawhub.ai/user/lemonjuice0)

### License/Terms of Use:

MIT-0

## Use Case:

Operators handling same-day service orders can use this skill to convert cached order messages into a fixed customer-facing notice, internal execution checklist, and table import row after the trigger phrase is provided.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Silent same-day order caching can retain order details without an explicit acknowledgement.

Mitigation: Require explicit user consent for caching and document what is cached, when it is cleared, and who can trigger formatting.

Risk: The skill is designed to ignore most input and remain silent until the trigger phrase, which can hide operational state.

Mitigation: Use clear host-side activation controls and confirm cache-clearing actions before deployment.

Risk: The fixed pricing and output text may be inappropriate for some services or customer contexts.

Mitigation: Review and make the output template and pricing text configurable before commercial use.

## Reference(s):

- [ClawHub skill page for task-assistant-bot](https://clawhub.ai/lemonjuice0/skills/task-assistant-bot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-like Chinese order template with a plain text table import row]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces no output until the configured trigger phrase is used; missing order fields are filled as pending.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
