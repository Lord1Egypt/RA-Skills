## Description:

Generates three-option emergency travel plans for flight cancellations, hotel overbooking, attraction closures, and weather disruptions using live FlyAI search data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uasnu1111](https://clawhub.ai/user/uasnu1111)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel support agents use this skill during active trip disruptions to compare three actionable alternatives with pricing, booking links, tradeoffs, and timing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents or users to install and run a global FlyAI CLI, with artifact guidance that may suggest elevated privileges or global npm configuration changes.

Mitigation: Use the skill only when FlyAI CLI is provisioned by a trusted administrator or installed in a contained, non-root environment; avoid sudo global installs and avoid changing global npm registry settings for this skill.

Risk: Travel prices, availability, and booking links come from live external services and may change quickly.

Mitigation: Verify prices, availability, refund rules, and booking terms on the final booking page before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uasnu1111/skills/travel-emergency-assistant)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown decision card with booking links, prices, tradeoffs, risk notes, and optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live external travel data and instructs users to verify price, availability, and booking terms on the booking page.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
