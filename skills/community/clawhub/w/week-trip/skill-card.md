## Description:

Plan an epic 7-day vacation with multi-city routes, intercity transportation, hotel transitions, and balanced daily itineraries, with support for travel booking and planning through FlyAI/Fliggy CLI results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to plan week-long trips from real-time FlyAI/Fliggy travel results, including flights, hotels, points of interest, transport transitions, fallback handling, and booking-link-oriented itinerary output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installation or use of a mutable global npm CLI for travel data retrieval.

Mitigation: Use a pinned and reviewed FlyAI CLI version, and require explicit approval before installing or updating global packages.

Risk: The skill can persist raw travel queries and command execution details in local logs.

Mitigation: Disable or redact logs when queries may contain personal travel details, and get user approval before retaining execution logs.

Risk: Travel recommendations and booking links depend on third-party FlyAI/Fliggy results and may affect purchases.

Mitigation: Review prices, availability, routes, and booking destinations before acting on recommendations or completing purchases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/week-trip)
- [templates.md](artifact/references/templates.md)
- [playbooks.md](artifact/references/playbooks.md)
- [fallbacks.md](artifact/references/fallbacks.md)
- [runbook.md](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links, comparison tables, concise travel guidance, and inline shell commands when retry or setup steps are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should use real-time CLI data, include booking links for returned travel results, and follow the user's language.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
