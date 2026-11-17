## Description:

RollingGo Hotel Search & Booking Assistant implements a hotel search, comparison, room-price lookup, booking, and order-checking workflow through RollingGo hotel APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dreamtzlong](https://clawhub.ai/user/dreamtzlong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to search hotels, compare options, check real-time room prices, create hotel orders, and inspect prior order status. It is intended for accommodation requests, not flights, trains, car rentals, attraction tickets, or destination-only travel chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs or updates mutable executable code from npm and GitHub release channels.

Mitigation: Install or update only after explicit user approval, use trusted RollingGo channels, and avoid administrator privileges where possible.

Risk: The workflow can collect guest names and email addresses and create real hotel orders with payment links.

Mitigation: Require explicit confirmation before sending personal data, locking prices, creating bookings, or directing the user to payment.

Risk: Search prices are reference prices and locked booking references expire after a short window.

Mitigation: Label search prices as reference prices, perform price confirmation before booking, and re-confirm expired locked prices.

## Reference(s):

- [CLI Command Complete Parameter Specifications](references/cli-params.md)
- [RollingGo hotel skill repository](https://github.com/RollingGo-AI/hotel-skill-global)
- [RollingGo hotel CLI releases](https://github.com/RollingGo-AI/oauth-hotel-cli-overseas/releases/latest)
- [ClawHub skill page](https://clawhub.ai/dreamtzlong/skills/rollinggo-hotel)
- [ClawHub publisher profile](https://clawhub.ai/user/dreamtzlong)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Markdown hotel cards, room and order summaries, authorization links, and payment links; CLI commands are intended for agent execution rather than user display.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [User-facing responses should hide raw CLI commands, JSON fields, internal identifiers, and technical parameters.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
