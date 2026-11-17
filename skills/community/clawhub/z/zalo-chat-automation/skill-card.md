## Description:

Automated conversational replies on personal Zalo accounts using connected AI models (Google Gemini, DeepSeek, OpenAI, Ollama) via Zalo-Flow Local-First Runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aizaloapp](https://clawhub.ai/user/aizaloapp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate replies and manage conversations on personal Zalo accounts with connected AI providers. It supports checking system status, listing conversations, and sending messages through Zalo-Flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live token can enable access to a personal Zalo account and its conversations.

Mitigation: Start with the demo sandbox or a test account, and keep any live token directed to your own runtime.

Risk: Automatic replies and AI-provider integrations may expose private conversation content or send unintended messages.

Mitigation: Restrict which conversations receive automatic replies and review the data supplied to each AI provider.

Risk: Private conversation data may be sent to a cloud provider if cloud fallback remains enabled.

Mitigation: For private conversations, verify local Ollama configuration and disable cloud fallback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aizaloapp/skills/zalo-chat-automation)
- [Zalo-Flow homepage and downloads](https://aizalo.com)
- [English documentation](https://aizalo.com/en)
- [Chatbot setup guide](https://aizalo.com/blog/huong-dan-cach-tao-chatbot-zalo-ca-nhan)
- [AI provider integration guide](https://aizalo.com/blog/tich-hop-ai-gemini-deepseek-vao-zalo-ca-nhan)
- [RapidAPI interactive playground](https://rapidapi.com/lekhoa288/api/zalo-flow-personal-zalo-chatbot-and-crm)

## Skill Output:

**Output Type(s):** [API calls, Text, Guidance]

**Output Format:** [JSON API requests and responses, plus Zalo chat messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conversation and message operations require a Zalo-Flow Personal Access Token for a live instance; a demo token is documented for sandbox testing.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
