## Description: <br>
Provides local TCL Lyon public transport timetable lookups for stops, lines, first and last departures, and upcoming departures from a local GTFS SQLite database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eaudaim](https://clawhub.ai/user/eaudaim) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to answer TCL Lyon transit questions with local timetable data, including stop searches, line information, upcoming departures, and first or last service of the day. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Schedule results are theoretical and may not reflect live delays, disruptions, accessibility-impacting changes, or urgent trip conditions. <br>
Mitigation: Verify with live TCL/Sytral or another current source for disruptions, urgent trips, accessibility-critical travel, or real-time information requests. <br>
Risk: The helper depends on a local tcl.db GTFS database whose freshness and trustworthiness affect results. <br>
Mitigation: Before installing or updating, confirm that tcl.db comes from a trustworthy and current source. <br>
Risk: The artifact tells agents not to use web search for TCL transit questions, which can be unsafe when current disruptions or live conditions matter. <br>
Mitigation: Use the local timetable for scheduled service, but consult a current official source when real-time conditions could change the answer. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/eaudaim/tcl-lyon) <br>
- [TCL Lyon GTFS dataset](https://transport.data.gouv.fr/datasets/horaires-theoriques-du-reseau-transports-en-commun-lyonnais) <br>
- [OpenClaw Skill TCL Lyon repository](https://github.com/eaudaim/OpenClaw-Skill-TCL-Lyon) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a local tcl.db SQLite GTFS database.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
