## Description:

Searches real-time red eye flights, overnight flights, and late-night departures with after-midnight arrival deals, with related travel booking support powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivan97](https://clawhub.ai/user/ivan97)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to search real-time red eye flight options, compare overnight departures, and present booking links from flyai CLI results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on installing and executing a third-party flyai CLI, including global or sudo installation paths mentioned in artifact guidance.

Mitigation: Review the flyai CLI source and provenance before installation, prefer a pinned local nonprivileged install, and avoid automatic global or sudo installation.

Risk: Raw travel queries and execution details may be persisted in logs.

Mitigation: Disable persistent logs when not needed, redact raw user queries, and avoid storing sensitive itinerary details.

Risk: Booking links point to external commercial services.

Mitigation: Treat booking links as external commercial links and review destination URLs before purchase or user handoff.

## Reference(s):

- [Templates - red-flights](references/templates.md)
- [Playbooks - red-flights](references/playbooks.md)
- [Fallbacks - Flight Category (Red Eye)](references/fallbacks.md)
- [Runbook - Execution Log Schema](references/runbook.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results should be based on flyai CLI output and include booking links when flights are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
