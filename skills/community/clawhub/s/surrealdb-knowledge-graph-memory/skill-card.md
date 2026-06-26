## Description: <br>
A knowledge graph memory system for agents that stores semantic facts, episodes, working memory, and automatically injects relevant context with per-agent isolation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add long-lived memory, semantic search, episodic recall, working-memory state, and scheduled knowledge extraction to agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read workspace memory files and send their contents to OpenAI for extraction and embeddings. <br>
Mitigation: Audit MEMORY.md and memory/*.md for secrets before enabling extraction or auto-injection, and use a scoped OpenAI key. <br>
Risk: The skill stores long-lived facts that can later affect agent behavior through memory injection. <br>
Mitigation: Review graph contents before enabling auto-injection, start with conservative limits, and prune stale or sensitive facts. <br>
Risk: Install, repair, service-start, and source-patching paths can make local environment changes. <br>
Mitigation: Install SurrealDB manually, use a dedicated Python virtual environment, keep SurrealDB bound to 127.0.0.1, and review any OpenClaw integration changes before applying them. <br>
Risk: Default SurrealDB credentials are suitable only for local development. <br>
Mitigation: Change root/root credentials with SURREAL_USER and SURREAL_PASS before any shared, production, or network-accessible deployment. <br>
Risk: Background extraction can run on a schedule and process memory files without manual invocation. <br>
Mitigation: Verify cron and auto-injection settings before enabling them, and disable scheduled jobs until one manual run has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick-software/surrealdb-knowledge-graph-memory) <br>
- [Clawdis homepage](https://clawhub.com/skills/surrealdb-knowledge-graph-memory) <br>
- [SECURITY.md](SECURITY.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Conflict Patterns](references/conflict-patterns.md) <br>
- [SurQL Examples](references/surql-examples.md) <br>
- [Enhanced Loop Hook Agent Isolation](references/enhanced-loop-hook-agent-isolation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and code references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce MCP tool calls, SurrealDB schema/setup steps, cron setup guidance, and memory-injection configuration.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
