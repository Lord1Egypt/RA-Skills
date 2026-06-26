## Description: <br>
Agent Memory System v12 provides a structured long-term memory layer for AI agents with hybrid retrieval, temporal reasoning, proactive memory management, privacy controls, and self-hosted deployment options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[concisegjh](https://clawhub.ai/user/concisegjh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent, searchable memory to AI agents through CLI commands, SDK calls, REST/MCP services, and local or self-hosted storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and retrieves long-term agent memory that may contain sensitive or regulated data. <br>
Mitigation: Use local storage and local embeddings/LLMs where possible, review memory contents regularly, and verify deletion, export, and backup behavior before storing sensitive data. <br>
Risk: Optional provider integrations require API keys and other sensitive credentials. <br>
Mitigation: Keep credentials in dedicated environment variables or secret stores, avoid shared shells and logs, and grant the narrowest read, write, or admin scope needed. <br>
Risk: Profiling, federation, sync, and external integrations can expose personal context beyond the local agent. <br>
Mitigation: Keep profiling and external integrations disabled unless users explicitly consent, and scope peers, tenants, and sync targets before enabling federation or sharing. <br>
Risk: Retrieved memory is untrusted context and may contain stale, inaccurate, or unsafe content. <br>
Mitigation: Treat recall output as user context rather than instructions, use review workflows for writes, and remove inaccurate or suspicious memories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/concisegjh/super-memory) <br>
- [Clawdis homepage](https://github.com/agent-memory/agent-memory) <br>
- [README](README.md) <br>
- [Architecture](ARCHITECTURE.md) <br>
- [Security Policy](SECURITY.md) <br>
- [API Reference](agent_memory/API.md) <br>
- [SDK Quickstart](docs/SDK_QUICKSTART.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python examples, configuration notes, API responses, and memory context text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local memory databases, call optional LLM or embedding providers, and expose HTTP or MCP service outputs when configured.] <br>

## Skill Version(s): <br>
12.2.0 (source: ClawHub release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
