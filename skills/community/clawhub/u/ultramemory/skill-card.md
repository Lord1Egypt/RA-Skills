## Description:

Ultramemory provides structured AI agent memory with temporal versioning, relational tracking, and semantic search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jared-goering](https://clawhub.ai/user/jared-goering)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to store, search, recall, and version conversation-derived facts across sessions. It supports entity profiles, temporal lookup, relation tracking, and startup context hydration for agents that need persistent memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived facts are stored locally and may include sensitive or regulated information.

Mitigation: Use a dedicated database per user or agent and avoid ingesting secrets, regulated data, or other sensitive content.

Risk: Ingest can send conversation-derived text to an external LLM provider.

Mitigation: Install only where the chosen provider is approved for the data being processed and configure API keys intentionally.

Risk: Recalled memories can be reintroduced into an agent session as untrusted context.

Mitigation: Treat recalled memories as context rather than instructions and review them before relying on high-impact outputs.

Risk: The released package depends on the separately installed ultramemory library.

Mitigation: Pin the dependency to a reviewed version before deployment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jared-goering/skills/ultramemory)
- [ClawHub publisher profile](https://clawhub.ai/user/jared-goering)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [CLI output as compact text or JSON, with Markdown documentation and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local SQLite database path and requires an Anthropic or OpenAI API key for ingest.]

## Skill Version(s):

0.2.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
