## Description:

Provides SMS compliance, formatting, and delivery best practices for Sendly API integrations, including TCPA compliance, quiet hours, opt-out handling, E.164 phone formatting, message segmentation, and carrier verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sendly-live](https://clawhub.ai/user/sendly-live)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams building SMS features with the Sendly API use this skill to apply compliance, formatting, delivery, carrier verification, and error-handling guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quiet-hours troubleshooting guidance could lead an agent to bypass marketing quiet-hour protections by relabeling a message as transactional.

Mitigation: Review and revise quiet-hours guidance so blocked marketing messages are delayed or scheduled for a permitted recipient-local time, and transactional classification is used only when the content and consent basis are genuinely transactional.

## Reference(s):

- [SMS Best Practices on ClawHub](https://clawhub.ai/sendly-live/skills/sms-best-practices)
- [Sendly Compliance Docs](https://sendly.live/docs/concepts/compliance)
- [Sendly Quiet Hours](https://sendly.live/docs/quiet-hours)
- [Sendly Country Requirements](https://sendly.live/docs/country-requirements)
- [Sendly Opt-Out Handling](https://sendly.live/docs/how-to/handle-opt-outs)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown guidance with tables, bullet lists, and inline API and error identifiers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
