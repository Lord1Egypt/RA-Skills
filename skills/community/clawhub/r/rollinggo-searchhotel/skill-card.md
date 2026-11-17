## Description:

RollingGo Search Hotel helps an agent search hotels, compare options, check live room pricing, guide hotel booking, and retrieve hotel order information through the RollingGo hotel CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dreamtzlong](https://clawhub.ai/user/dreamtzlong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to find accommodations, compare hotel attributes and prices, inspect room availability, create payable hotel orders, and review existing hotel bookings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs mutable external executables from npm or latest GitHub releases.

Mitigation: Use only trusted RollingGo distribution channels, avoid administrator/root installs, and prefer a pinned, checksum-verified CLI package or binary.

Risk: The skill can create real hotel bookings, payment links, and order-history lookups.

Mitigation: Require explicit user consent before booking, payment-link generation, updates, or order retrieval, and confirm guest and contact details before purchase actions.

Risk: The skill may silently check remote content for version updates.

Mitigation: Review network behavior before deployment and ensure users or operators approve update checks in controlled environments.

## Reference(s):

- [CLI parameter reference](references/cli-params.md)
- [ClawHub skill page](https://clawhub.ai/dreamtzlong/skills/rollinggo-searchhotel)
- [RollingGo hotel CLI release downloads](https://github.com/RollingGo-AI/oauth-hotel-cli/releases/latest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown hotel summaries, room-price summaries, booking status text, payment links, and selected shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include hotel images, prices, cancellation policies, authorization links, payment links, and order details when returned by the RollingGo CLI.]

## Skill Version(s):

1.0.5 (source: ClawHub server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
