## Description:

Query Dutch Railways (NS) for train departures, trip planning, disruptions, and station search via the trein CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joehoel](https://clawhub.ai/user/joehoel)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to query Dutch Railways (NS) departures, trip plans, disruptions, and station search through the trein CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on installing and running the third-party trein executable.

Mitigation: Install only from trusted npm or release sources and review the package source or release provenance before use in sensitive environments.

Risk: NS_API_KEY can be exposed through shell history, config files, screenshots, backups, or repositories.

Mitigation: Set NS_API_KEY only for the shell or session that needs it, and keep any trein config file private and excluded from backups and source control.

Risk: Train departure, disruption, and trip-planning results are time-sensitive operational data.

Mitigation: Verify important travel decisions against current NS data close to departure time.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joehoel/skills/trein)
- [Publisher profile](https://clawhub.ai/user/joehoel)
- [trein project homepage](https://github.com/joelkuijper/trein)
- [trein GitHub releases](https://github.com/joelkuijper/trein/releases)
- [NS API portal](https://apiportal.ns.nl/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference the NS_API_KEY environment variable and trein CLI commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
