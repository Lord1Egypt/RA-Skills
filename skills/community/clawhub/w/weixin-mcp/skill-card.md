## Description:

Guides an agent to send and receive WeChat messages, list contacts, and manage a weixin-mcp daemon through the npx weixin-mcp CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bkmashiro](https://clawhub.ai/user/bkmashiro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an agent to WeChat through the weixin-mcp CLI for messaging, inbox checks, contact lookup, and webhook-based bot integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party CLI that can access WeChat login tokens, contacts, messages, attachments, and local credential storage.

Mitigation: Install only after reviewing and trusting the weixin-mcp package, prefer an exact reviewed package version, and keep WEIXIN_MCP_DIR in a dedicated protected directory.

Risk: Webhook delivery can expose message content and context tokens outside the local machine.

Mitigation: Use localhost or trusted internal webhook URLs only, and avoid forwarding WeChat payloads to untrusted services.

Risk: Broad WeChat-related prompts could cause the skill to read or send private messages in sensitive conversations.

Mitigation: Require explicit user confirmation before reading inbox contents, sending messages, or acting on broad WeChat requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bkmashiro/skills/weixin-mcp)
- [weixin-mcp npm package](https://www.npmjs.com/package/weixin-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational instructions for the weixin-mcp CLI and MCP configuration; it does not directly send messages without the agent running the referenced commands or tools.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
