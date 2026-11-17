## Description:

Send messages to WeCom (企业微信) via webhooks using MCP protocol. Works with Claude Code, Claude Desktop, and other MCP clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qidu](https://clawhub.ai/user/qidu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using MCP clients use this skill to let an agent send text or markdown updates into approved WeCom group chats through a configured incoming webhook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook URLs can grant posting access to a WeCom group if exposed.

Mitigation: Store WECOM_WEBHOOK_URL outside source control and logs, and rotate it if exposure is suspected.

Risk: Agent-generated messages may contain secrets, personal data, or internal material.

Mitigation: Limit use to approved WeCom channels and review data-handling expectations before enabling the skill.

Risk: Runtime dependencies and remote package execution can change over time.

Mitigation: Prefer pinned or local dependency execution and keep packages updated.

## Reference(s):

- [WeCom group chat message API](https://developer.work.weixin.qq.com/document/path/99110)
- [WeCom API documentation](https://work.weixin.qq.com/api/doc)
- [WeCom app download](https://work.weixin.qq.com/#indexDownload)
- [ClawHub skill page](https://clawhub.ai/qidu/skills/wecom)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [MCP tool calls that post text or markdown messages and return status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WECOM_WEBHOOK_URL; optional WECOM_TIMEOUT_MS controls request timeout.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
