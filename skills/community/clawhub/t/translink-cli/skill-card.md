## Description: <br>
Query, troubleshoot, and explain Translink SEQ GTFS static and realtime data using local translink_* commands or plugin slash commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alanburchill](https://clawhub.ai/user/alanburchill) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to query Translink SEQ schedule and realtime GTFS data, inspect joins across routes, trips, stops, and stop_times, review alerts, and troubleshoot schema drift through local CLI or plugin command surfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on local translink_* commands found in PATH. <br>
Mitigation: Before installation or use, confirm the exact source of the Translink CLI scripts and ensure the PATH-resolved commands are trusted. <br>
Risk: The skill can refresh and maintain a local transit cache. <br>
Mitigation: Use refresh or scheduled refresh behavior only when the user expects local cache updates, and review cache freshness when answering time-sensitive transit questions. <br>
Risk: Realtime output and schema snapshots may change as upstream Translink data changes. <br>
Mitigation: Read the generated schema docs first for authoritative current columns and use the CLI's structured invalid-field suggestions to recover from schema drift. <br>


## Reference(s): <br>
- [Translink CLI scripts repository](https://github.com/alanburchill/traslink-cli-scripts) <br>
- [Translink website](https://www.translink.com.au/) <br>
- [Translink CLI Commands](references/commands.md) <br>
- [Translink CLI usage](references/usage.md) <br>
- [GTFS Relationships](references/relationships.md) <br>
- [Translink Schema](references/schema-generated.md) <br>
- [Column Meanings and Data Format](references/column-meanings.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Analysis, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and references to table, JSON, or CSV CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to run local translink_* commands, refresh a local cache, inspect schema output, or use plugin slash commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
