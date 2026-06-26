## Description: <br>
Swiss Public Transport real-time information for querying train, bus, tram, or boat schedules in Switzerland, including station search, departure boards, journey planning, and connection details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xenofex7](https://clawhub.ai/user/xenofex7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to look up Swiss public transport stations, real-time departure boards, and point-to-point journey options without an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Origin, destination, date, and time queries are sent to transport.opendata.ch. <br>
Mitigation: Avoid using the skill for travel details considered sensitive. <br>
Risk: The upstream transport.opendata.ch service is described in evidence security guidance as unofficial. <br>
Mitigation: Treat returned schedules as lookup assistance and verify critical travel plans with an official transport provider when needed. <br>


## Reference(s): <br>
- [transport.opendata.ch API](https://transport.opendata.ch) <br>
- [Swiss Public Transport on ClawHub](https://clawhub.ai/xenofex7/swiss-transport) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional formatted text output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return live schedule data, station matches, departure times, route sections, platform information, and delays from transport.opendata.ch.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
