## Description:

A comprehensive knowledge graph memory system with semantic search, episodic memory, working memory, automatic context injection, and per-agent isolation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent SurrealDB-backed semantic, episodic, and working memory to OpenClaw agents. It supports knowledge search, fact storage, task history recall, context injection, and per-agent memory isolation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and prompt injection can influence future agent behavior.

Mitigation: Review knowledge graph contents before enabling auto-injection, keep the feature explicitly opt-in, and start with conservative injection limits.

Risk: Memory extraction can send workspace memory content to OpenAI.

Mitigation: Audit MEMORY.md and memory/*.md for secrets or sensitive data, use a limited OpenAI key, and disable scheduled extraction until reviewed.

Risk: Local setup can involve mutable installers and maintenance controls.

Mitigation: Prefer manual SurrealDB installation, avoid UI or gateway auto-repair and install buttons, bind services to localhost, and change default root/root credentials.

Risk: Broad export or maintenance operations can expose or alter persisted memory.

Mitigation: Treat this as an elevated local integration, review security notes before installation, and enable cron jobs or maintenance operations only after manual validation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maverick-software/skills/surrealdb-knowledge-graph-memory)
- [ClawHub Metadata Homepage](https://clawhub.com/skills/surrealdb-knowledge-graph-memory)
- [Security Notes](SECURITY.md)
- [Conflict Patterns](references/conflict-patterns.md)
- [Enhanced Loop Hook Agent Isolation](references/enhanced-loop-hook-agent-isolation.md)
- [SurQL Examples](references/surql-examples.md)
- [SurrealDB Install Documentation](https://surrealdb.com/install)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration snippets, and agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance and tool usage instructions for a local SurrealDB-backed memory integration.]

## Skill Version(s):

2.3.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
