## Description:

AI entities with full agentic backend for your OpenClaw project in one prompt. Your IDE agent will self-register and start building. Human is optional.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subfeed-ai](https://clawhub.ai/user/subfeed-ai)

### License/Terms of Use:


## Use Case:

Developers and IDE agents use this skill to connect an OpenClaw project to Subfeed Cloud, register an agent identity, create an AI entity, and guide human onboarding when explicitly approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may register accounts or create Subfeed entities before the user has clearly approved the exact action.

Mitigation: Require explicit user approval before account registration, entity creation, human onboarding, or any cloud resource creation.

Risk: The skill asks agents to load mutable remote instructions from Subfeed during use.

Mitigation: Review remote instructions before following them and avoid continuing if the fetched content differs from the validated release expectations.

Risk: Using a full human API key can grant broad account access to Subfeed Cloud operations.

Mitigation: Prefer SUBFEED_AGENT_TOKEN when possible and only use SUBFEED_API_KEY after the user approves the specific operation and data being sent.

Risk: Messages, entity configuration, and RAG content can be sent to Subfeed Cloud.

Mitigation: Confirm that the user intends to send the exact data to Subfeed Cloud before chat, entity configuration, RAG, or attachment operations.

## Reference(s):

- [Subfeed ClawHub skill page](https://clawhub.ai/subfeed-ai/skills/subfeed)
- [Subfeed homepage](https://subfeed.app)
- [Subfeed remote skill document](https://subfeed.app/skill.md)
- [Subfeed RAG guide](https://subfeed.app/skill/rag.md)
- [Subfeed addons guide](https://subfeed.app/skill/addons.md)
- [Subfeed MCP guide](https://subfeed.app/skill/mcp.md)
- [Subfeed webhook guide](https://subfeed.app/skill/webhook.md)
- [Subfeed directory guide](https://subfeed.app/skill/directory.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with REST API examples and JSON request/response snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Subfeed credentials through SUBFEED_API_KEY or SUBFEED_AGENT_TOKEN for authenticated operations.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
