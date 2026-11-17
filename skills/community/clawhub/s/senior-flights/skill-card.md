## Description:

Find senior flight deals, 60+ discount tickets and elderly travel options with accessible boarding and comfortable seating for senior travelers, plus related travel services powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivan97](https://clawhub.ai/user/ivan97)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to find senior-friendly flights, compare comfort-oriented options, and present booking links from flyai CLI results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and running the third-party flyai CLI, which may have broad local effects.

Mitigation: Review the skill before installing, install flyai only when that provider is intended, and avoid running sudo npm install for it.

Risk: The runbook asks agents to keep local logs of raw travel queries and command history.

Mitigation: Disable or constrain local logging when travel queries contain sensitive personal, itinerary, or accessibility information.

Risk: The skill can produce misleading travel results if an agent bypasses the CLI or invents fares, discounts, booking links, or accessibility details.

Mitigation: Require every travel result to come from flyai CLI output and include a detailUrl-backed booking link before presenting it to a user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivan97/skills/senior-flights)
- [Fallbacks - Flight Category (Senior)](references/fallbacks.md)
- [Playbooks - senior-flights](references/playbooks.md)
- [Runbook - Execution Log Schema (Universal)](references/runbook.md)
- [Templates - senior-flights](references/templates.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links, comparison tables, comfort tips, and inline shell commands when troubleshooting is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires results from the flyai CLI and should not output raw JSON.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
