## Description:

小红书（XHS/RED）自动化助手，提供用于登录、浏览、搜索、互动、用户资料查看和内容发布的小红书 MCP 服务端工具。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weznai](https://clawhub.ai/user/weznai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to a local Xiaohongshu MCP service for account login, feed discovery, note detail retrieval, profile lookup, engagement actions, and content publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes Xiaohongshu account cookies, which should be treated as exposed session credentials.

Mitigation: Remove bundled cookies before installation, rotate the affected session, and require users to log in with their own account.

Risk: The MCP service can expose account-changing tools if bound beyond the local machine or used without strong access control.

Mitigation: Bind the service to localhost or add strong authentication before use.

Risk: Publishing, commenting, deleting login state, liking, and favoriting can change a real Xiaohongshu account.

Mitigation: Require explicit user approval before executing account-changing actions.

## Reference(s):

- [XHS MCP API 文档](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/weznai/skills/skill-xiaohongshu)
- [Xiaohongshu](https://www.xiaohongshu.com)
- [Xiaohongshu Creator Publish](https://creator.xiaohongshu.com/publish/publish)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [MCP tool responses as JSON text, plus Markdown usage guidance with shell and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a logged-in Xiaohongshu session for account-specific actions.]

## Skill Version(s):

1.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
