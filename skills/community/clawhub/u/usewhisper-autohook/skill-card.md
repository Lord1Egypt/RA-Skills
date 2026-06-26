## Description: <br>
Auto-hook tools for OpenClaw: query Whisper Context before every generation, ingest after every turn. Built for Telegram agents with stable user_id and session_id values. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Alinxus](https://clawhub.ai/user/Alinxus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers use this skill to add automatic Whisper memory retrieval and turn ingestion to OpenClaw agents, especially Telegram agents with stable user and session identifiers. It can also run local OpenAI-compatible or Anthropic-compatible proxies to reduce repeated chat-history payloads while injecting relevant memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to send and store full chat turns in an external memory service. <br>
Mitigation: Use it only where users have consented to memory storage, and add redaction, minimization, opt-out, retention, and deletion controls for confidential or user-private chats. <br>
Risk: Proxy mode forwards requests through a local compatibility server and uses upstream provider API keys. <br>
Mitigation: Keep proxy servers bound to localhost, avoid exposing them on a network, and use narrowly scoped provider keys where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Alinxus/usewhisper-autohook) <br>
- [Whisper Context API default endpoint](https://context.usewhisper.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and user-provided Whisper Context API configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
