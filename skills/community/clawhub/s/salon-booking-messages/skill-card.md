## Description:

Drafts US salon booking confirmations, reminders and reschedule messages with policies and clear instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

Salon owners and staff use the skill to prepare confirmation, reminder, reschedule, and cancellation messages that clearly state appointment details and salon policies.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The bundled script checks message fields but does not produce the promised customer messages.

Mitigation: Treat its result as a validation report; prepare and review the actual message and salon policy before sending.

Risk: The script may replace booking-message.md in the selected output folder.

Mitigation: Choose an output folder where replacing that file is acceptable.

Risk: The optional separate Windows app is unsigned and is not needed for the Python workflow.

Mitigation: Use the Python workflow; make a separate trust decision before downloading or running the app.

## Reference(s):

- [US salon booking communication](references/salon-booking.md)
- [ClawHub release](https://clawhub.ai/rapidworker1/skills/salon-booking-messages)
- [Publisher homepage](https://github.com/rapidworker1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Salon booking-message drafts, or a local validation report when using the bundled script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review appointment details, salon policies, fees, and communication preferences before sending.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
