## Description:

Search for wheelchair accessible flights with mobility assistance options. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[liquanyu123](https://clawhub.ai/user/liquanyu123)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to search flight options with wheelchair or mobility assistance considerations, compare routes, and return booking links from the flyai CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install an unpinned global npm CLI during ordinary travel queries.

Mitigation: Require explicit user approval, use a pinned and audited CLI version, and run installation or execution in a sandboxed environment.

Risk: Broad shell-command templates may execute external searches using user-provided travel parameters.

Mitigation: Validate origin, destination, date, and sort options against the documented parameters before running commands.

Risk: Wheelchair accessibility may not be verified unless the provider returns clear accessibility-specific fields.

Mitigation: Present accessibility information as provider-dependent and advise users to confirm assistance directly with the airline or booking provider.

## Reference(s):

- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for travel results and requires each returned result to include a booking detailUrl.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
