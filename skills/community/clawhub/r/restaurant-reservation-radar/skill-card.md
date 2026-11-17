## Description:

旅行目的地米其林与热门餐厅空位监控、自动预约与定金提醒助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lmercy](https://clawhub.ai/user/lmercy)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to identify Michelin or popular restaurants, monitor reservation availability, submit reservation requests, and return confirmations or alternatives for a destination itinerary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to submit third-party restaurant reservation requests using personal contact details.

Mitigation: Require explicit user confirmation before every reservation submission, account login, deposit, card guarantee, cancellation-penalty booking, or payment-related step.

Risk: Reservation monitoring may interact with platform limits or booking rules.

Mitigation: Use platform-appropriate polling intervals and comply with each reservation platform's access and booking requirements.

Risk: The workflow may handle phone numbers, email addresses, verification codes, or payment-related information.

Mitigation: Collect only the details needed for the booking, avoid persistent storage, and ask the user to provide sensitive confirmations through secure, deliberate steps.

## Reference(s):

- [Platform Reference Manual](reference.md)
- [Usage Examples](examples.md)
- [ClawHub Skill Page](https://clawhub.ai/lmercy/skills/restaurant-reservation-radar)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured reservation status updates and notification templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include restaurant candidates, availability status, confirmation details, maps links, cancellation notes, and alternative options.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
