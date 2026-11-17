## Description:

Find flights departing within 48 hours for spontaneous trips or emergency travel with immediate availability and real-time seat status, powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to search urgent flight options within 48 hours, compare available itineraries, and present booking links based on live flyai CLI results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install an unpinned global flyai CLI, including a sudo fallback in artifact guidance.

Mitigation: Review the CLI package and installation source before use, avoid sudo installation, and prefer a pinned or isolated installation path.

Risk: The skill depends on external booking links returned by the CLI.

Mitigation: Use the skill only when the flyai CLI and returned booking links are trusted, and review links before acting on them.

Risk: The runbook behavior may persist raw travel queries and command history in a local hidden log file.

Mitigation: Disable or review local logging where sensitive travel details are involved, and remove logs according to the user's retention needs.

## Reference(s):

- [Urgent Flights on ClawHub](https://clawhub.ai/dingtom336-gif/skills/urgent-flights)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results should be sourced from flyai CLI output and include booking links when available.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
