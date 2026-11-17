## Description:

RollingGo Hotel Booking Skill helps agents search hotels, compare options, check room availability and pricing, guide booking, and query hotel orders through RollingGo hotel APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rollinggo-ai](https://clawhub.ai/user/rollinggo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to find accommodations, compare room options and prices, complete hotel booking flows after confirmation, and review hotel order status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and may update mutable executable code from RollingGo npm packages or GitHub releases.

Mitigation: Install only when the publisher is trusted, review package and release integrity before use, and require explicit approval before any CLI update.

Risk: The skill can create real hotel booking orders using OAuth-backed personal and travel data.

Mitigation: Require explicit confirmation before price confirmation and order creation, and treat authorization links, payment links, order history, names, and travel dates as sensitive.

Risk: Displayed search prices are not locked prices and booking references can expire.

Mitigation: Label search results as reference prices and re-run price confirmation when a booking reference is stale before creating an order.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rollinggo-ai/skills/rollinggo-hotel-booking-global)
- [Server-resolved GitHub source](https://github.com/RollingGo-AI/RollingGo-hotel-skill-global/tree/main/skills/rollinggo-hotel-booking)
- [RollingGo Hotel CLI release](https://github.com/RollingGo-AI/oauth-hotel-cli-overseas/releases/latest)
- [CLI command parameter specifications](references/cli-params.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown hotel cards, room summaries, order summaries, authorization links, booking links, and payment links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search prices are reference prices until price confirmation; booking can create real orders after explicit user confirmation.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
