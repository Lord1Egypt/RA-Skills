## Description:

Persistent causal memory for AI agents that records decisions, tool calls, parallel work, and session history as a causally linked chain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[has9800](https://clawhub.ai/user/has9800)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agent operators use Raven Memory to give OpenClaw or MCP-compatible agents persistent local recall across sessions, including causal chains for actions, decisions, branch/merge work, rollback, and semantic history search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory can retain sensitive conversation content, decisions, tool history, and user preferences across sessions.

Mitigation: Enable the skill only for workspaces where persistent memory is appropriate, avoid recording secrets or regulated data, and restrict the Raven database path with appropriate filesystem permissions.

Risk: Recalled memory is intended to be loaded into the agent's context and can influence future behavior.

Mitigation: Review recalled summaries and nodes before relying on them for sensitive decisions, scope databases by project or user, and remove or roll back stale or inappropriate memory.

Risk: Artifact text advertises optional SQLCipher encryption, while the security evidence warns not to rely on it unless the installed package implements and enforces it.

Mitigation: Verify encryption behavior in the installed package before storing sensitive data, or rely on external controls such as disk encryption and access-controlled database locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/has9800/skills/raven-memory)
- [Publisher profile](https://clawhub.ai/user/has9800)
- [Artifact README](artifact/README.md)
- [Skill manifest](artifact/skill.md)
- [Package metadata](artifact/pyproject.toml)
- [MCP server implementation](artifact/tcc/integration/mcp_server.py)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration, Guidance]

**Output Format:** [JSON tool responses and natural-language memory summaries for MCP-compatible agents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include recalled conversation-derived memory, node summaries, search results, rollback status, health status, and database path information.]

## Skill Version(s):

1.0.1 (source: frontmatter, pyproject.toml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
