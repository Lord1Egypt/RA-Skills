## Description:

Production-grade persistent memory for AI agents with hybrid SQLite and vector search, decay classes, episodic memory, cognitive profiles, and an MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marlandoj](https://clawhub.ai/user/marlandoj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add durable local memory, recall, and profile-aware retrieval to Node.js agents through a CLI, MCP server, or programmatic API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive long-term agent memory in a local database.

Mitigation: Use a private database path with restrictive file permissions and avoid storing secrets, regulated data, or other high-sensitivity content.

Risk: Configured embedding, reranking, or HyDE features can send queries and memory snippets to local or external model services.

Mitigation: Keep OLLAMA_URL pointed only at a trusted local or HTTPS service and enable OpenAI, reranker, or HyDE features only when that data sharing is acceptable.

Risk: Installing or running through npm or npx can execute package code from the selected release.

Mitigation: Pin npm or npx versions and review the package before deployment in sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marlandoj/skills/zouroboros-memory)
- [OpenClaw Zouroboros Repository](https://github.com/AlaricHQ/zouroboros-openclaw)
- [Memory OpenClaw Example](https://github.com/AlaricHQ/zouroboros-openclaw-examples/tree/main/examples/memory-openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON-like configuration snippets, TypeScript code examples, shell commands, and MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write a local SQLite memory database and may call configured embedding, reranking, or generation services when enabled.]

## Skill Version(s):

3.0.0 (source: SKILL.md frontmatter and ClawHub release evidence; package.json reports 4.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
