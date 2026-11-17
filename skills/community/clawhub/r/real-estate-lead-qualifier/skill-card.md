## Description:

Real Estate Lead Qualifier helps realtors and property managers respond to portal inquiries, qualify leads by budget, pre-approval, and timeline, schedule viewings, and apply ThumbGate Fair Housing guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorganapolsky](https://clawhub.ai/user/igorganapolsky)

### License/Terms of Use:

MIT-0

## Use Case:

External real estate teams use this skill to manage inbound Zillow/Realtor.com inquiries, qualify buyer readiness, and coordinate viewing appointments. It is intended for customer-facing lead response workflows that need Fair Housing-sensitive guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned ThumbGate installer can change behavior between installs or introduce supply-chain risk.

Mitigation: Install ThumbGate only from a verified, pinned version and test enforcement before using live lead traffic.

Risk: Automated Fair Housing-sensitive replies, budget exceptions, or pre-approval handling can create compliance or customer harm if guardrails fail.

Mitigation: Require manual review for sensitive replies, budget exceptions, and pre-approval documents before confirming appointments.

Risk: Calendar and SMS integrations can expose lead data or trigger unintended customer outreach.

Mitigation: Use test accounts first and avoid production calendars or SMS accounts until booking and response controls are verified.

## Reference(s):

- [Real Estate Lead Qualifier on ClawHub](https://clawhub.ai/igorganapolsky/skills/real-estate-lead-qualifier)
- [Setup guide](artifact/setup-guide.md)
- [ThumbGate prevention rules](artifact/thumbgate-rules.md)
- [Twilio](https://twilio.com)
- [Calendly](https://calendly.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce lead qualification recommendations, booking guidance, Fair Housing redirects, and setup steps for related portal, calendar, SMS, and ThumbGate integrations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
