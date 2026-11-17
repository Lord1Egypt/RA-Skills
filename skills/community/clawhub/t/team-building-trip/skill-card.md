## Description:

Book flights for team building trips and company retreats. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[liquanyu123](https://clawhub.ai/user/liquanyu123)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and travel coordinators use this skill to collect team trip parameters, run flyai travel searches, and format booking options for company retreats or group travel. It is intended for agent-assisted travel planning where results come from CLI output rather than model memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run an unpinned global CLI package.

Mitigation: Require explicit user approval before installing @fly-ai/flyai-cli, pin and verify the CLI version, and avoid global installation where possible.

Risk: User-supplied city and date values may be inserted into unsafe command templates.

Mitigation: Validate city and date inputs, pass arguments without shell-rendered command strings, and reject unsupported parameters.

Risk: Booking links are external destinations returned by the travel CLI.

Mitigation: Disclose that booking links leave the agent environment and should be reviewed before purchase.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liquanyu123/skills/team-building-trip)
- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Travel search results are expected to include external booking links returned by the flyai CLI.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
