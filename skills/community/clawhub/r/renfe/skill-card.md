## Description:

Helps users search Spanish Renfe trains, compare fares, and book tickets through the Renfe CLI with user-approved Bizum payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mejiasd3v](https://clawhub.ai/user/mejiasd3v)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and their assistants use this skill to find Renfe schedules and fares in Spain, compare nearby travel dates, and book or retrieve tickets with the traveler's approval.

### Deployment Geography for Use:

Spain

## Known Risks and Mitigations:

Risk: The launcher may download and run a third-party executable from a GitHub release.

Mitigation: Review the CLI before use or install the pinned Go module yourself from a trusted environment.

Risk: Passenger identity and contact details are stored locally for booking.

Mitigation: Keep the passenger file private and review or delete it when no longer needed.

Risk: Booking and Bizum payment can incur charges; retrying after an uncertain payment may duplicate a purchase.

Mitigation: Confirm the train, total fare, and payment request before approval; after a pending payment or timeout, check the bank app and Renfe email rather than paying again.

## Reference(s):

- [Renfe CLI project (listed homepage)](https://github.com/mejiasd3v/renfe-cli)
- [Renfe skill listing](https://clawhub.ai/mejiasd3v/skills/renfe)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and booking details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI returns JSON; confirmed bookings may save a ticket PDF locally.]

## Skill Version(s):

0.1.0 (source: skill metadata and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
