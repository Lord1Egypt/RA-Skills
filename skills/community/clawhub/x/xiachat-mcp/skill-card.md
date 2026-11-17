## Description:

XiaChat MCP connects an agent to XiaChat personality matching, SOUL profile creation and import/export, avatar pre-chat, Soul Square persona chat, and compatibility scoring workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizhijun](https://clawhub.ai/user/lizhijun)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure and call XiaChat MCP tools for creating SOUL profiles, finding compatible matches, testing conversations through AI avatar pre-chat, and chatting with Soul Square personas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned third-party MCP server through npx.

Mitigation: Prefer a pinned and verified @xiachat/mcp-server version before use.

Risk: The skill can send sensitive personality profiles, quiz answers, chat exports, match data, and pre-chat transcripts to XiaChat.

Mitigation: Use a restricted API key, minimize private chat history, and send personal or third-party conversation data only with appropriate consent.

Risk: The evidence does not provide clear privacy and consent boundaries for relationship, personality, and chat data.

Mitigation: Review XiaChat's data handling terms and avoid high-sensitivity uploads when retention, sharing, or consent expectations are unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lizhijun/skills/xiachat-mcp)
- [XiaChat homepage](https://xiachat.com)
- [XiaChat API settings](https://xiachat.com/settings/api)
- [Soul Square](https://xiachat.com/square)
- [SOUL profile](https://xiachat.com/soul)
- [XiaChat match center](https://xiachat.com/match)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON configuration, MCP tool names, workflow steps, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference XiaChat MCP tool calls that exchange SOUL profiles, quiz answers, chat text, match identifiers, pre-chat transcripts, and persona-chat messages with the configured service.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
