## Description:

Xiaozhi Mcp Openclaw Official connects XiaoZhi AI devices through an MCP endpoint to OpenClaw or other OpenAI-compatible backends using an `openclaw_query(message)` MCP tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joe12801](https://clawhub.ai/user/joe12801)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to bridge an existing XiaoZhi MCP endpoint to an OpenClaw or OpenAI-compatible assistant backend without modifying XiaoZhi source code. It is suited for adding external assistant capability that returns short Chinese responses for voice playback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys, user queries, and MCP endpoint tokens may be exposed through under-disclosed network defaults or logging.

Mitigation: Set OPENAI_BASE to the intended HTTPS backend, use a narrowly scoped and rotated OPENAI_KEY, avoid reusable tokens in URLs where logs may capture them, and review logging before deployment.

Risk: The bridge forwards XiaoZhi requests to an external OpenAI-compatible backend.

Mitigation: Use the skill only when both the XiaoZhi MCP endpoint and backend are trusted, and consider pinning dependencies before deployment.

## Reference(s):

- [Artifact README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/joe12801/skills/xiaozhi-mcp-openclaw-official)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; MCP tool output is short Chinese text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The MCP tool sends one message string to the configured backend and requests responses capped at 512 max_tokens.]

## Skill Version(s):

1.0.2 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
