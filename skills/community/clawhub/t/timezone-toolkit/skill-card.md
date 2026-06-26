## Description: <br>
Convert times between timezones, show world clocks, find meeting overlap across zones, and look up UTC offsets and DST status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, distributed teams, and agents use this skill to convert times, compare current times across locations, find overlapping meeting hours, and inspect UTC offsets or DST status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an executable Python CLI when invoked. <br>
Mitigation: Review proposed commands before running them and execute only expected timezone utility commands. <br>
Risk: Timezone aliases such as EST or PST can be ambiguous around daylight saving transitions. <br>
Mitigation: Prefer full IANA timezone names for time-sensitive scheduling and verify converted times when DST changes matter. <br>


## Reference(s): <br>
- [Timezone Toolkit on ClawHub](https://clawhub.ai/Johnnywang2001/timezone-toolkit) <br>
- [Publisher profile](https://clawhub.ai/user/Johnnywang2001) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Self-contained Python 3.9+ timezone calculations using the standard zoneinfo database.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
