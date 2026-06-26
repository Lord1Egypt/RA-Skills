## Description: <br>
Subfeed helps an IDE agent self-register with Subfeed Cloud, create an AI entity for an OpenClaw project, and optionally onboard a human account with permission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Subfeed-AI](https://clawhub.ai/user/Subfeed-AI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and IDE agents use Subfeed to register an agent identity, create and manage a Subfeed Cloud AI entity, and connect optional capabilities such as RAG, addons, MCP, webhooks, and public directory discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to create persistent Subfeed Cloud identities and entities. <br>
Mitigation: Install only when cloud identity creation is intended, prefer agent-scoped tokens, and confirm token revocation and entity deletion procedures before use. <br>
Risk: The artifact instructs agents to re-fetch remotely mutable skill instructions. <br>
Mitigation: Review any fetched remote instructions before execution and avoid automatic remote skill updates without human approval. <br>
Risk: Entity configs, chat messages, and RAG content are sent to Subfeed Cloud. <br>
Mitigation: Avoid sending sensitive content until data handling, RAG storage, addon behavior, and account controls are understood. <br>


## Reference(s): <br>
- [Subfeed ClawHub release](https://clawhub.ai/Subfeed-AI/subfeed) <br>
- [Subfeed homepage](https://subfeed.app) <br>
- [Subfeed live skill document](https://subfeed.app/skill.md) <br>
- [Subfeed RAG documentation](https://subfeed.app/skill/rag.md) <br>
- [Subfeed addons documentation](https://subfeed.app/skill/addons.md) <br>
- [Subfeed MCP documentation](https://subfeed.app/skill/mcp.md) <br>
- [Subfeed webhook documentation](https://subfeed.app/skill/webhook.md) <br>
- [Subfeed directory documentation](https://subfeed.app/skill/directory.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with HTTP request examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SUBFEED_API_KEY or SUBFEED_AGENT_TOKEN for authenticated operations; sends API requests and entity data to Subfeed Cloud.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
