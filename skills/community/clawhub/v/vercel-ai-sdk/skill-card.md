## Description: <br>
Vercel AI SDK guidance for building streaming chat interfaces with React hooks, UI messages, tool calls, and server-side streaming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement and review Vercel AI SDK chat flows, including useChat clients, streaming routes, UIMessage handling, tool-call loops, and persistence validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated code or copied examples may enable automatic tool calls or sensitive client-side actions without adequate review. <br>
Mitigation: Review onToolCall, addToolOutput, sendAutomaticallyWhen, location access, payments, deletion, and similar flows before shipping; require explicit user approval for sensitive tools. <br>
Risk: Chat payloads, tool outputs, or persistence examples may store or send sensitive content to providers. <br>
Mitigation: Decide what chat content is stored or transmitted, validate UI messages before persistence, and apply normal data handling controls for the application. <br>


## Reference(s): <br>
- [Vercel AI SDK ClawHub release](https://clawhub.ai/anderskev/vercel-ai-sdk) <br>
- [UIMessage Structure Reference](references/messages.md) <br>
- [Streaming Reference](references/streaming.md) <br>
- [Tools Reference](references/tools.md) <br>
- [useChat Hook Reference](references/use-chat.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with TypeScript examples and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only reference material with copyable examples] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
