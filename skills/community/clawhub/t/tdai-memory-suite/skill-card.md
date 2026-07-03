## Description: <br>
Complete local memory system for OpenClaw with a four-layer memory pipeline, local vector search, an ontology knowledge graph, and Nomic Atlas visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add persistent local memory, semantic recall, structured knowledge graph operations, and memory visualization to an agent. It is intended for agents that need conversation capture, memory extraction, persona generation, and retrieval across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records conversations persistently and may store sensitive memory data. <br>
Mitigation: Use the default local SQLite mode, review retention needs, and avoid storing secrets or regulated data unless the deployment policy allows it. <br>
Risk: Tencent Cloud, remote embedding, or offload paths may send memory data to external services when enabled. <br>
Mitigation: Keep those integrations disabled unless intentionally configured, and review service terms, credentials, and data handling requirements before use. <br>
Risk: Postinstall or patch scripts may alter the host OpenClaw installation. <br>
Mitigation: Review the patch script before execution, run installation in a controlled environment, and keep backups of host configuration and plugin files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/paudyyin/tdai-memory-suite) <br>
- [Publisher profile](https://clawhub.ai/user/paudyyin) <br>
- [Ontology schema reference](components/tdai-ontology/references/schema.md) <br>
- [Ontology query reference](components/tdai-ontology/references/queries.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets, shell commands, memory records, ontology JSONL, and generated HTML visualization files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist conversation-derived memories, persona files, ontology data, and visualization artifacts on disk.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
