## Description: <br>
Convert time between different timezones using IANA timezone database. Supports 12/24-hour formats, specific dates, and automatic DST handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, distributed teams, and agent users use this skill to convert times between IANA time zones for scheduling, UTC conversion, and cross-region coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Timezone conversion can be wrong if a user supplies an ambiguous abbreviation, omits the date, or crosses daylight saving time boundaries. <br>
Mitigation: Use explicit IANA timezone names and a specific date, then review the displayed UTC offsets before relying on the result for scheduling. <br>
Risk: The artifact describes a command-line helper that may require local executable permissions. <br>
Mitigation: Review the installed files before running chmod or executing local commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/time-converter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text conversion results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs converted date and time, source and target time zones, UTC offsets, and daylight saving notes when relevant.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter and _meta.json report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
