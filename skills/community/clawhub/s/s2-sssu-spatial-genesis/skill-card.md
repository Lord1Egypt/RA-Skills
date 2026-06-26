## Description: <br>
A spatial protocol engine for formatting, validating, and registering Smart Space Standard Units (SSSU) and managing entity spawning via local database tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to format and validate SUNS v3.0 SSSU addresses, register spatial nodes, and record entity spawning events in a local SQLite registry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores submitted spatial addresses and entity IDs in a local SQLite database. <br>
Mitigation: Use only non-sensitive identifiers and delete s2_spatial_genesis.db when the registry and timeline state should be reset. <br>
Risk: Invalid SUNS v3.0 addresses or unregistered spaces can prevent registration or entity spawning. <br>
Mitigation: Use the documented format http://[Domain]/[L1]-[L2]-[L3]-[L4C]-[RoomID]-[GridID] and register the SSSU address before calling spawn_entity. <br>


## Reference(s): <br>
- [S2 SSSU Spatial Genesis Engine on ClawHub](https://clawhub.ai/spacesq/s2-sssu-spatial-genesis) <br>
- [Publisher profile: spacesq](https://clawhub.ai/user/spacesq) <br>
- [README.md](README.md) <br>
- [Skill reference](skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files] <br>
**Output Format:** [JSON response containing a status field and text output; the skill may also update a local SQLite database file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates s2_spatial_genesis.db in the skill directory to retain registered spatial addresses, entity IDs, occupancy, and timeline state.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata and skill.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
