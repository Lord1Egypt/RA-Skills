## Description: <br>
Production-grade persistent memory for AI agents with hybrid SQLite and vector search, decay classes, episodic memory, cognitive profiles, and an MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marlandoj](https://clawhub.ai/user/marlandoj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to add persistent local memory, hybrid recall, episodic records, cognitive profiles, and MCP-accessible memory tools to Node.js-based AI agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored memory can persist locally and may include sensitive facts if users save them. <br>
Mitigation: Review the database path and avoid storing secrets or confidential data unless persistent storage is intended. <br>
Risk: Optional Ollama and OpenAI features can send memory text and queries to configured model endpoints. <br>
Mitigation: Enable vector search, HyDE expansion, or reranking only when the configured endpoint is approved for the memory content. <br>
Risk: Delete and prune commands can remove stored records. <br>
Mitigation: Confirm record IDs, retention needs, and backups before running destructive memory commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/marlandoj/zouroboros-memory) <br>
- [Publisher profile](https://clawhub.ai/user/marlandoj) <br>
- [Zouroboros OpenClaw repository](https://github.com/AlaricHQ/zouroboros-openclaw) <br>
- [Memory OpenClaw example](https://github.com/AlaricHQ/zouroboros-openclaw-examples/tree/main/examples/memory-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, code] <br>
**Output Format:** [CLI text or JSON output, MCP tool responses, and TypeScript API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores and retrieves local SQLite-backed memory records; optional vector search, HyDE expansion, and reranking depend on configured Ollama or OpenAI endpoints.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and SKILL.md frontmatter; package.json reports 4.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
