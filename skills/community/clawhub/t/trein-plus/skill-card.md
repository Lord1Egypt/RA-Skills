## Description:

Query Dutch Railways (NS) for train-only departures, time-based trip planning, disruptions, and station search via the trein CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timvandervoord](https://clawhub.ai/user/timvandervoord)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer train travel questions in the Netherlands, including departures, train trips by departure or arrival time, disruptions, and station lookup. It is not intended for car, bus, or other non-train transport planning.

### Deployment Geography for Use:

Netherlands

## Known Risks and Mitigations:

Risk: The skill depends on installing and running the third-party trein CLI.

Mitigation: Install only from trusted upstream sources and review the CLI before using it in managed environments.

Risk: The trein CLI requires an NS API key that may be exposed if stored in shared or synced locations.

Mitigation: Prefer setting NS_API_KEY as a session environment variable; if using a config file, keep it private and restrict file permissions.

Risk: Using the skill for non-train travel can produce irrelevant transport guidance.

Mitigation: Confirm the user wants train travel in the Netherlands before invoking trein commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timvandervoord/skills/trein-plus)
- [Publisher profile](https://clawhub.ai/user/timvandervoord)
- [trein CLI homepage](https://github.com/joelkuijper/trein)
- [trein GitHub releases](https://github.com/joelkuijper/trein/releases)
- [NS API portal](https://apiportal.ns.nl/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON response interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses structured JSON output from the trein CLI when querying departures, trips, disruptions, and stations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
