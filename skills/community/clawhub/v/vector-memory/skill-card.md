## Description: <br>
Vector Memory provides smart memory search for agents, using semantic embeddings when available and falling back to keyword search otherwise. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BluePointDigital](https://clawhub.ai/user/BluePointDigital) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use Vector Memory to search prior work, preferences, decisions, and memory notes with automatic fallback between semantic vector search and keyword search. It is intended for OpenClaw-style agent memory workflows that need immediate search plus optional local indexing for better recall. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted inputs may execute shell commands. <br>
Mitigation: Review and fix command construction before use in sensitive workspaces; restrict inputs to trusted values until fixed. <br>
Risk: memory_get may read files outside the intended memory area. <br>
Mitigation: Validate and normalize requested paths, then restrict reads to approved memory files or directories. <br>
Risk: The installer runs downloaded code. <br>
Mitigation: Prefer the ClawHub install path or manually review installation steps before running downloaded scripts. <br>
Risk: Sync reads local memory files and stores searchable chunks locally. <br>
Mitigation: Run sync only on intended memory directories and avoid indexing sensitive workspaces until the deployment has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BluePointDigital/vector-memory) <br>
- [Integration Guide](vector-memory/references/integration.md) <br>
- [pgvector Version](vector-memory/references/pgvector.md) <br>
- [Memory Structure](MEMORY_STRUCTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON results and Markdown/plain-text memory snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include file paths, line ranges, scores, and snippets; sync can create a local searchable index.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
