## Description:

Agent Memory System v12 provides persistent memory for AI agents with multi-engine recall, temporal reasoning, proactive management, and privacy controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[concisegjh](https://clawhub.ai/user/concisegjh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent, searchable memory to agents, including recall, context assembly, forgetting, maintenance, API/CLI/MCP access, and privacy-aware controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can retain sensitive, incorrect, or outdated information.

Mitigation: Keep the service local by default, review stored memories regularly, delete inappropriate records, and enable collectors or personality analysis only with consent.

Risk: Networked API, MCP, or Playground surfaces can expose memory data if deployed without strong authentication.

Mitigation: Set strong API keys and JWT secrets before enabling any server, bind to localhost unless remote access is intentional, and avoid unauthenticated HTTP exposure.

Risk: Retrieved memories can contain untrusted or stale context that may influence agent behavior.

Mitigation: Treat recalled memories as quoted data rather than instructions and require explicit confirmation before high-impact write, sync, maintain, export, or server operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/concisegjh/skills/super-memory)
- [Agent Memory Homepage](https://github.com/agent-memory/agent-memory)
- [Agent Memory Documentation](https://agent-memory.readthedocs.io)
- [BAAI bge-small-zh-v1.5 Model](https://huggingface.co/BAAI/bge-small-zh-v1.5)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and structured text with command examples and optional JSON/API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write a persistent local memory database and may use optional LLM or embedding backends when configured.]

## Skill Version(s):

12.2.0 (source: server release evidence, SKILL.md frontmatter, CHANGELOG, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
