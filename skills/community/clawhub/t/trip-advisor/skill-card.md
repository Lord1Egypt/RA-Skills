## Description:

Plan your entire trip with AI, including flights, hotels, attractions, day-by-day itinerary, booking support, visa information, travel insurance, car rental, and related travel needs powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel planners use this skill to collect trip parameters, run flyai travel-search commands, and turn real-time flight, hotel, attraction, visa, and itinerary results into user-facing travel plans with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run an unpinned global flyai CLI.

Mitigation: Review the package and version before installation and run the skill in a sandboxed environment.

Risk: The skill uses user-filled shell command templates for travel searches.

Mitigation: Validate command parameters against the documented tables before execution and do not invent or pass unsupported arguments.

Risk: Travel requests may contain sensitive passport, identity, or private itinerary details.

Mitigation: Avoid collecting unnecessary sensitive details and do not persist execution logs containing raw travel requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/trip-advisor)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when retry steps are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are expected to include flyai-sourced booking links and a flyai attribution tag; raw JSON is not intended for users.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
