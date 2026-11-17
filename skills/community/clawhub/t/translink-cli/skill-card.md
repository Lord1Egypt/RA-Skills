## Description:

Query, troubleshoot, and explain Translink SEQ GTFS static + realtime data using local translink_* commands or plugin slash commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alanburchill](https://clawhub.ai/user/alanburchill)

### License/Terms of Use:


## Use Case:

Developers and transit-data analysts use this skill to query Translink SEQ static and realtime GTFS data, inspect schedules and stops, reason over route, trip, and stop joins, check alerts and vehicle data, and recover from schema or field-name errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates runtime behavior to separately installed translink_* commands.

Mitigation: Verify the external Translink CLI source before installation and prefer a known commit or release.

Risk: A different executable with a matching translink_* name in PATH could change command behavior.

Mitigation: Confirm the command path and installed version before using the skill for transit-data analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alanburchill/skills/translink-cli)
- [Translink CLI scripts](https://github.com/alanburchill/traslink-cli-scripts)
- [Translink](https://www.translink.com.au/)
- [Command and parameter contract](references/commands.md)
- [Usage examples](references/usage.md)
- [GTFS relationships](references/relationships.md)
- [Auto-generated schema](references/schema-generated.md)
- [Column meanings](references/column-meanings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional table, JSON, or CSV command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on separately installed translink_* commands; command output may be paginated and schema-driven.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
