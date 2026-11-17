## Description:

Relay messages to AI agents on any OpenAI-compatible API. Supports multi-turn conversations with session management. List agents, send messages, reset sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericsantos](https://clawhub.ai/user/ericsantos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to list configured agents, send prompts to an OpenAI-compatible endpoint, and continue or reset local multi-turn sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and retained session history are sent to the configured AI endpoint.

Mitigation: Use only trusted HTTPS endpoints and avoid sending secrets, credentials, or regulated data unless the endpoint and machine are approved for that data.

Risk: Conversation history is retained locally in plaintext for session continuity.

Mitigation: Use --reset before sensitive work or delete the local session files when history should not be retained.

Risk: The relay uses RELAY_API_KEY to call the configured endpoint.

Mitigation: Scope RELAY_API_KEY to this use and rotate or revoke it if the local environment or configured endpoint is no longer trusted.

## Reference(s):

- [Relay To Agent on ClawHub](https://clawhub.ai/ericsantos/skills/relay-to-agent)
- [OpenAI Chat Completions API Reference](https://platform.openai.com/docs/api-reference/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON responses from the selected agent, with Markdown documentation and shell-command examples for setup and operation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent replies are returned from the configured endpoint; session history is stored locally for continuity unless reset or deleted.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
