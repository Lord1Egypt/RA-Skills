## Description:

Book flights for retirement celebration trips. Also supports flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more, powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to collect route and date preferences, run FlyAI flight searches for retirement trips, compare options, and return booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may globally install and execute a third-party npm CLI, modifying the agent environment.

Mitigation: Use a version-pinned, approved FlyAI CLI in an isolated environment and verify the package before execution.

Risk: Travel search details are sent to FlyAI/Fliggy and booking URLs are returned to the user.

Mitigation: Limit sensitive travel details and validate booking-link domains before presenting returned links.

Risk: Shell commands are assembled from user-provided travel input.

Mitigation: Validate origin, destination, date, and supported flags before running commands.

## Reference(s):

- [ClawHub retirement-trip skill page](https://clawhub.ai/xiejinsong/skills/retirement-trip)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands when setup or execution is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLI-derived flight data; booking links must use detailUrl; raw JSON is not shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
