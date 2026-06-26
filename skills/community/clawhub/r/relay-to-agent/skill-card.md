## Description: <br>
Relay messages to AI agents on any OpenAI-compatible API. Supports multi-turn conversations with session management. List agents, send messages, reset sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericsantos](https://clawhub.ai/user/ericsantos) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and operators use this skill to route prompts to configured OpenAI-compatible agents, list available agents, continue session-based conversations, and reset local session state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and retained session history are sent to the configured AI endpoint. <br>
Mitigation: Avoid secrets or regulated data, and use only trusted API keys and base URLs. <br>
Risk: Custom session IDs may read or write JSON files outside the advertised local session cache. <br>
Mitigation: Use the default session or simple session IDs without path characters until session files are constrained to the cache directory. <br>


## Reference(s): <br>
- [Relay To Agent ClawHub page](https://clawhub.ai/ericsantos/relay-to-agent) <br>
- [Publisher profile: ericsantos](https://clawhub.ai/user/ericsantos) <br>
- [OpenAI Chat Completions API reference](https://platform.openai.com/docs/api-reference/chat) <br>
- [openai-fetch package metadata](https://registry.npmjs.org/openai-fetch/-/openai-fetch-3.4.2.tgz) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, JSON] <br>
**Output Format:** [Plain text by default, or JSON when --json is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local multi-turn session history with up to 50 messages per agent and session.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
