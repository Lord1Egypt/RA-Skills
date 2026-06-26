## Description: <br>
Gives OpenClaw agents persistent, searchable long-term memory for user preferences, project context, important facts, and cross-session recall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuyunting555](https://clawhub.ai/user/wuyunting555) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and agent developers use this skill to persist, search, and inject memories across sessions so agents can reuse preferences, facts, project context, and interaction patterns without repeated prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation data and user preferences may be stored automatically as long-term local memories. <br>
Mitigation: Review what the hooks capture before enabling the skill, avoid sharing secrets, and periodically inspect or delete stored memories. <br>
Risk: Embedding generation can use an external provider when configured with an OpenAI API key. <br>
Mitigation: Prefer the local embedding provider for sensitive conversations, or review data handling requirements before enabling external embeddings. <br>
Risk: The dashboard and API expose memory and payment operations on a local server. <br>
Mitigation: Keep the service bound to trusted local environments and do not expose it to networks until authentication and stronger access controls are added. <br>
Risk: Autonomous payment features can spend funds for Pro storage. <br>
Mitigation: Do not provide a funded wallet unless a human has approved strict spending limits and payment review requirements. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/wuyunting555/shrimp-openclaw-memory) <br>
- [README](README.md) <br>
- [Agent Payments Guide](AGENT-PAYMENTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, local API examples, and memory context injected as text or structured request data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store and retrieve local SQLite memory records, generate embeddings locally or through OpenAI, and expose CLI and localhost dashboard/API responses.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
