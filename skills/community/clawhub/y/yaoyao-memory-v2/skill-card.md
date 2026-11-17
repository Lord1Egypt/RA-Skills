## Description:

Yaoyao Memory Homo provides a six-layer memory system for agents to persist context across sessions, store knowledge locally in SQLite, and search it with FTS5 and optional vector retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taobaoaz](https://clawhub.ai/user/taobaoaz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to give an OpenClaw or ClawHub agent persistent long-term memory, local retrieval, maintenance tooling, and optional sync or API access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can read and retain conversation-derived data.

Mitigation: Install only when persistent memory is appropriate, review retained data regularly, and avoid storing sensitive information that should not persist across sessions.

Risk: The dashboard or local API can expose memory and configuration if route authentication and CORS are not fixed.

Mitigation: Do not run the dashboard or API until authentication and CORS controls are corrected and verified for the intended environment.

Risk: Remote embeddings, LLM summaries, cloud sync, MCP, shell embedding, and psychology modules may expose data or credentials when enabled.

Mitigation: Keep those optional features disabled unless they are explicitly needed, then configure credentials deliberately and review what data each feature may send.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taobaoaz/skills/yaoyao-memory-v2)
- [QUICKSTART.md](QUICKSTART.md)
- [ADVANCED.md](ADVANCED.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)
- [SECURITY.md](SECURITY.md)
- [API.md](API.md)
- [Memory lifecycle reference](references/memory-lifecycle.md)
- [Heartbeat maintenance reference](references/heartbeat-maintenance.md)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [IMA knowledge base](https://ima.qq.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; scripts may create local SQLite, JSON, Markdown, and HTML artifacts when executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses persistent local storage under ~/.openclaw/workspace/memory/ and optional credentials for LLM, embedding, and IMA sync features.]

## Skill Version(s):

4.0.1 (source: ClawHub server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
