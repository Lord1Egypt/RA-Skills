## Description:

Book flights for family and class reunion trips, with support for flight booking, hotel reservations, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, and car rentals powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivan97](https://clawhub.ai/user/ivan97)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to collect reunion trip flight parameters, run flyai CLI searches, and format real-time booking options with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to install and run an unpinned global flyai CLI package.

Mitigation: Use only in a controlled environment, verify the flyai CLI package independently, and do not allow automatic global npm installation.

Risk: User travel details are used to construct shell commands.

Mitigation: Pass validated arguments without shell interpolation and restrict execution to documented parameters.

Risk: Booking links returned by the CLI may point to external destinations.

Mitigation: Treat booking links as untrusted until their destination is checked.

## Reference(s):

- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [ClawHub skill page](https://clawhub.ai/ivan97/skills/reunion-trip)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI results; booking links are sourced from CLI detailUrl fields.]

## Skill Version(s):

3.2.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
