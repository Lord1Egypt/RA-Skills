## Description:

Give this agent its own email address - create inboxes, send, reply in-thread, search mail, and manage senders via SentFromAI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuelar2](https://clawhub.ai/user/samuelar2)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to give an agent a SentFromAI email inbox for sending, receiving, replying to, forwarding, searching, and managing email senders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad live-email send, reply, forward, search, and blocking capability without clear per-action user confirmation or tight scoping.

Mitigation: Install only when the agent should handle real email, use a scoped API key where possible, and review sends, replies, and forwards before they happen.

Risk: Email handled by the agent may contain or expose sensitive content.

Mitigation: Avoid secrets or regulated data in mail handled by the agent.

Risk: The documented MCP setup uses an unpinned npx install command.

Mitigation: Prefer a pinned or reviewed MCP server install before production use.

## Reference(s):

- [SentFromAI documentation](https://docs.sentfrom.ai)
- [SentFromAI for agents](https://docs.sentfrom.ai/for-agents)
- [SentFromAI LLM reference](https://docs.sentfrom.ai/llms-full.txt)
- [ClawHub skill page](https://clawhub.ai/samuelar2/skills/sentfromai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SENTFROMAI_API_KEY and may use a configured SentFromAI MCP server or direct HTTPS API calls.]

## Skill Version(s):

0.4.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
