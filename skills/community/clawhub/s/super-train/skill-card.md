## Description:

Flyai Super Train helps agents search Chinese train availability, compare direct and transfer routes, apply seat and time preferences, and present booking options using flyai search-train.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangxchao](https://clawhub.ai/user/zhangxchao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel assistants use this skill to collect train search parameters, check availability, compare direct and transfer itineraries, and recommend options based on seat, time, transfer, price, and booking-link details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist travel routes, dates, seat choices, and booking decisions in local preference and history files.

Mitigation: Review the local data files before installation, clear or disable persistent personalization when it is not desired, and avoid storing sensitive travel history unnecessarily.

Risk: The skill relies on an unpinned globally installed third-party flyai CLI.

Mitigation: Use a pinned, locally managed CLI version where possible, review the CLI source and package provenance, and avoid running npm installation commands with elevated privileges.

## Reference(s):

- [flyai CLI command reference](references/flyai-cli-reference.md)
- [FlyAI Open Platform](https://flyai.open.fliggy.com/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with itinerary tables, recommendation text, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update local preference and history JSON files when the user confirms persistent personalization.]

## Skill Version(s):

1.0.4 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
