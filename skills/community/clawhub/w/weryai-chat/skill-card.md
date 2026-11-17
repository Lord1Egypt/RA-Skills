## Description:

Chat, ask, compare, and inspect WeryAI chat models through the official OpenAI-compatible chat completions API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weryai-developer](https://clawhub.ai/user/weryai-developer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to call WeryAI chat-completions models for assistant-style answers, multi-turn message-array conversations, model lookup, and model selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and chat messages are sent to WeryAI's paid external API.

Mitigation: Use this skill only when external WeryAI processing is intended, and avoid sending sensitive prompts unless the deployment has approved that data flow.

Risk: Changing WERYAI_BASE_URL could send the API key and prompts to an untrusted endpoint.

Mitigation: Keep the default endpoint unless a trusted HTTPS endpoint has been explicitly reviewed and approved.

Risk: Verbose logging can expose prompt or response content.

Mitigation: Avoid verbose mode when prompts or responses may contain sensitive information.

Risk: Unused balance and status helpers may broaden the package surface without clear user-facing documentation.

Mitigation: Remove those helpers or document their purpose before broad deployment.

## Reference(s):

- [WeryAI Chat API](references/chat-api.md)
- [Chat Completion API](https://docs.weryai.com/api-reference/chat/chat-completion)
- [Get Chat Models List](https://docs.weryai.com/api-reference/chat/get-chat-models-list)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and API response text or JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+ and WERYAI_API_KEY; real chat calls use a paid external WeryAI API and may consume credits.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
