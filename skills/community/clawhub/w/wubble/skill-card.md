## Description:

Use when a user wants to connect to or use Wubble's official remote MCP server for music, speech, voice, dubbing, and sound-effect workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubbletech](https://clawhub.ai/user/wubbletech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent or MCP client to Wubble's remote audio MCP server, complete OAuth, and choose appropriate read-only or media-generation workflows. It supports music, speech, voice, dubbing, dialog, and sound-effect tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wubble MCP actions can create media or consume Wubble requests or credits.

Mitigation: Confirm the user's intent and requested output before generation, upload, remix, dubbing, speech, or other spendful actions.

Risk: OAuth tokens, API keys, signed media URLs, private media, prompts, lyrics, transcripts, or voice data may be sensitive.

Mitigation: Do not log, store, or reveal those values unless the user explicitly approves sharing in the current context.

Risk: Users may ask for legal conclusions about generated or downloaded media rights.

Mitigation: Direct users to Wubble's official Terms of Use and Subscriber License rather than improvising legal advice.

## Reference(s):

- [Wubble Skill on ClawHub](https://clawhub.ai/wubbletech/skills/wubble)
- [Wubble MCP server endpoint](https://mcp.wubble.ai/mcp)
- [Wubble MCP health endpoint](https://mcp.wubble.ai/health)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with endpoint, registry, OAuth, and safe-use instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide MCP tool calls that create media or consume Wubble credits after user confirmation.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
