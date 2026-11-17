## Description:

Book Qingming Festival flights for Tomb Sweeping Day travel and spring outings, with additional support for flight booking, hotel reservations, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and related Fliggy-powered travel tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivan97](https://clawhub.ai/user/ivan97)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search Qingming Festival and general travel options through the flyai CLI, then present bookable flight and travel results with links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install an unpinned global npm package for the flyai CLI.

Mitigation: Require explicit approval before installation and prefer a pinned local CLI version in a controlled environment.

Risk: Travel itinerary details are sent to a third-party travel CLI.

Mitigation: Use the skill only when users accept sharing itinerary details with the third-party CLI provider.

Risk: Shell commands are built from user-provided travel parameters.

Mitigation: Validate route and date parameters and execute commands without shell interpolation.

## Reference(s):

- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires booking results to come from flyai CLI output and include Book links when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
