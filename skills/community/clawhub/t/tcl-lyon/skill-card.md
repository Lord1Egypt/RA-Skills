## Description:

Provides TCL Lyon bus, metro, tram, funicular, and trolleybus schedule lookup from a local GTFS SQLite database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eaudaim](https://clawhub.ai/user/eaudaim)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer Lyon TCL transit schedule questions, including first and last departures, upcoming departures, stop searches, and line information.

### Deployment Geography for Use:

Global, with transit coverage limited to Lyon, France.

## Known Risks and Mitigations:

Risk: The skill depends on a local tcl.db schedule database whose presence and freshness are not verified in the release evidence.

Mitigation: Install and refresh the GTFS database before use, and check an official live source for time-sensitive trip planning.

Risk: The artifact describes theoretical schedules and includes overconfident source-selection wording.

Mitigation: Treat the output as schedule guidance, not real-time service status, and corroborate delays, disruptions, and edge cases with official live TCL information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eaudaim/skills/tcl-lyon)
- [TCL theoretical schedules dataset](https://transport.data.gouv.fr/datasets/horaires-theoriques-du-reseau-transports-en-commun-lyonnais)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text transit schedule summaries and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on a local tcl.db GTFS SQLite database; schedule data is theoretical and not real-time.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
