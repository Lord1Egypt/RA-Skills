## Description:

Vercel AI SDK for building chat interfaces with streaming. Use when implementing useChat hook, handling tool calls, streaming responses, or building chat UI. Triggers on useChat, @ai-sdk/react, UIMessage, ChatStatus, streamText, toUIMessageStreamResponse, addToolOutput, onToolCall, sendMessage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as concise implementation guidance for Vercel AI SDK chat interfaces, including React useChat wiring, UIMessage structures, streaming server routes, tool calls, and persistence checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive client-side tools, such as location access, may be executed too automatically if examples are copied without adding user control.

Mitigation: Require explicit user consent for sensitive tools and use the documented approval flow before tool execution.

Risk: Chat persistence examples can lead to unvalidated or unauthorized message data being saved.

Mitigation: Validate UI messages with validateUIMessages or stricter server-side validation, authorize persistence, and minimize stored message and file data.

Risk: Production implementations may inherit example defaults that expose more data to servers or model providers than necessary.

Mitigation: Review each copied pattern, limit file and message payloads to the minimum required, and restrict automatic tool execution to low-risk actions.

## Reference(s):

- [useChat Hook Reference](references/use-chat.md)
- [UIMessage Structure Reference](references/messages.md)
- [Streaming Reference](references/streaming.md)
- [Tools Reference](references/tools.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with TypeScript examples and implementation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is documentation-only and should be reviewed before applying to production code.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
