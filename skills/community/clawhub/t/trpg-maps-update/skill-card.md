## Description:

Updates or fixes the map system in an existing briefing_package by organizing larger map YAML files, updating scene map references, and optionally adding map panel configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ice26985850](https://clawhub.ai/user/ice26985850)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content maintainers use this skill to update TRPG briefing packages so larger structured maps live under maps/, scene YAML files refer to them with map_ref, and optional map panel settings are captured in config.yaml.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally changes project structure by moving large map YAML files from data/ to maps/ and deleting the old data/ copy.

Mitigation: Review the resulting file moves and deletions, and confirm moved map files exist under maps/ before accepting deletion of the original data/ files.

Risk: Incorrect map_ref values can break scene-to-map linkage after large maps are moved.

Mitigation: Check each updated scene YAML against the final maps/ filenames and verify map_ref values omit only the .yaml extension as expected.

Risk: Editing transitional or legacy map files can create conflicting versions of the same map.

Mitigation: Limit edits to the formal briefing_package map and scene YAML files and the latest formal external map files identified by the project.

## Reference(s):


## Skill Output:

**Output Type(s):** [Configuration, Files, Guidance, Shell commands]

**Output Format:** [Markdown guidance with file edits and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create maps/ directories, move YAML files, update scene YAML references, and add map_config settings.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
