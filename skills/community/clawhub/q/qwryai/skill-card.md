## Description:

Connect OpenClaw to a paid QwryAI workspace through the read-only QwryAI MCP and public API integration surface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tamjeedhur](https://clawhub.ai/user/tamjeedhur)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support operators use this skill to let an agent inspect QwryAI chatbots, conversations, knowledge, messages, analytics, and account context through a read-only integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A QwryAI API key can expose tenant chatbot, conversation, knowledge, message, analytics, and account data to the local agent environment.

Mitigation: Use a read-only, revocable key, keep it in an environment variable or secret manager, and avoid committing local MCP configuration.

Risk: Endpoint overrides can route requests away from the official QwryAI API.

Mitigation: Keep the default QwryAI endpoints unless the alternate environment is fully trusted.

Risk: Users may ask the agent to perform unsupported write, billing, user-management, or admin actions.

Mitigation: Limit use to read-only inspection workflows and do not request replies, conversation resolution, chatbot edits, user management, or billing changes.

## Reference(s):

- [QwryAI ClawHub Skill](https://clawhub.ai/tamjeedhur/skills/qwryai)
- [tamjeedhur ClawHub Publisher Profile](https://clawhub.ai/user/tamjeedhur)
- [QwryAI Homepage](https://qwryai.com)
- [QwryAI MCP Endpoint](https://api.qwryai.com/mcp)
- [QwryAI Public API Endpoint](https://api.qwryai.com/public/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a paid QwryAI workspace and a read-only QWRYAI_API_KEY; optional endpoint overrides are available for trusted environments.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
