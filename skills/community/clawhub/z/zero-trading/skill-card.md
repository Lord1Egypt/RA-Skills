## Description:

Trading agent for Hyperliquid via Zero that evaluates markets through nine intelligence layers and helps operators manage paper or explicitly approved live trading sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squaeragent](https://clawhub.ai/user/squaeragent)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to connect an OpenClaw agent to ZERO's remote MCP trading engine, evaluate crypto markets, choose strategies, and manage trading sessions. The skill emphasizes paper mode by default and requires explicit operator approval before live trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist or overwrite MCP server configuration for a remote trading service.

Mitigation: Require a visible configuration diff, backup, and explicit confirmation before any write or overwrite, and prefer the canonical https://api.getzero.dev/mcp endpoint.

Risk: The skill connects an agent to a remote service that can manage trading sessions.

Mitigation: Start in paper mode, require explicit approval before live trading or auto-rotation, and review strategy risk previews before deployment.

Risk: Market data, session data, or remote tool calls may be unavailable, stale, or incomplete.

Mitigation: Report failed tool calls plainly, do not fabricate market values, and use documented fallbacks such as individual coin evaluation when heat data is empty.

## Reference(s):

- [ZERO Homepage](https://getzero.dev)
- [ZERO MCP Endpoint](https://api.getzero.dev/mcp)
- [ZERO Trading ClawHub Page](https://clawhub.ai/squaeragent/skills/zero-trading)
- [Strategy Reference](references/strategies.md)
- [Layer Details](references/layer-details.md)
- [Output Templates Reference](references/output-templates.md)
- [Error Handling Reference](references/error-codes.md)
- [Voice Guide](references/voice-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with trading captions, inline buttons, JSON MCP configuration, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference remote ZERO card-rendering endpoints for visual trading summaries; paper mode is the default unless live trading is explicitly approved.]

## Skill Version(s):

2.1.0 (source: server release metadata; artifact frontmatter says 2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
