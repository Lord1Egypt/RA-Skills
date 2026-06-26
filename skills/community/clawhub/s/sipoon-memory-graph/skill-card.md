## Description: <br>
Memory Graph provides SQLite-backed entity and relationship storage with add_entity, add_relation, query, traverse, get_path, and stats operations for agent memory workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sipoon](https://clawhub.ai/user/sipoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to persist local knowledge graph entities and relationships, then query, traverse, and inspect paths in that graph. It is intended for agent memory and skill-compounding workflows that need structured project, decision, technology, person, tool, or skill records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory can retain sensitive project or personal details. <br>
Mitigation: Avoid storing sensitive information unless retention and deletion practices are defined before use. <br>
Risk: The artifact uses a hard-coded database path for graph storage. <br>
Mitigation: Change the database location to a user-controlled workspace path before installing or running the skill. <br>
Risk: The security review marks the release suspicious due to under-scoped persistence and memory-use controls. <br>
Mitigation: Review the storage behavior and scan the skill before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sipoon/sipoon-memory-graph) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Guidance] <br>
**Output Format:** [Python API calls returning strings, lists, and dictionaries backed by a local SQLite database] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or opens a persistent local graph database and returns entity IDs, edge IDs, query results, traversal results, path results, and graph statistics.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
