## Description: <br>
High-performance SpacetimeDB memory integration for OpenClaw that stores, searches, updates, deletes, imports, and consolidates long-term memories through a local SpacetimeDB instance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kennethrajsimon](https://clawhub.ai/user/kennethrajsimon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to replace flat-file memory with local SpacetimeDB-backed memory operations for storing, searching, editing, and deleting agent memories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The legacy import script can overwrite existing workspace memory files after copying .bak backups. <br>
Mitigation: Run the legacy import only with explicit user approval, a reviewed target workspace path, and verified .bak backups. <br>
Risk: Memory operations depend on a reachable local SpacetimeDB instance and the expected database name. <br>
Mitigation: Confirm SPACETIMEDB_URL and SPACETIMEDB_NAME before relying on store, search, edit, or delete operations. <br>


## Reference(s): <br>
- [SpacetimeDB](https://spacetimedb.com/) <br>
- [ClawHub skill page](https://clawhub.ai/kennethrajsimon/spacetime-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON tool results and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool output includes memory IDs, content, tags, timestamps, status values, and error text from the local SpacetimeDB operation.] <br>

## Skill Version(s): <br>
1.1.7 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
