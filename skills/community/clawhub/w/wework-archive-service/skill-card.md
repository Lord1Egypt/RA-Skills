## Description:

企业微信整合服务技能 - 包含普通回调和会话内容存档功能

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyl2835](https://clawhub.ai/user/cyl2835)

### License/Terms of Use:

MIT

## Use Case:

Developers and administrators use this skill to deploy and operate an Enterprise WeChat integration service for callback handling, conversation archiving, message querying, SQLite storage, and Cloudflare Tunnel exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is flagged as suspicious because it ships hard-coded WeCom secrets.

Mitigation: Treat embedded tokens and secrets as compromised, remove them before deployment, and require protected user-supplied secrets loaded from a secure runtime configuration source.

Risk: Archived messages may be exposed through unauthenticated public-facing archive, query, or debug endpoints.

Mitigation: Add authentication and authorization to every archive, query, and debug endpoint, disable debug endpoints in production, and avoid exposing administrative APIs through Cloudflare Tunnel.

Risk: Conversation content may be logged, retained, or stored without sufficient controls.

Mitigation: Stop logging message contents and add encryption, retention, and access-control enforcement before using the service with real Enterprise WeChat data.

## Reference(s):

- [Skill source on ClawHub](https://clawhub.ai/cyl2835/skills/wework-archive-service)
- [Cloudflare Tunnel完整配置文档](artifact/references/Cloudflare Tunnel完整配置文档.md)
- [企业微信API接口文档](artifact/references/企业微信API接口文档.md)
- [企业微信后台配置步骤](artifact/references/企业微信后台配置步骤.md)
- [合规要求](artifact/references/合规要求.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, Python service code, SQL assets, and reference documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deployment and operation instructions for a local Enterprise WeChat archive service; no model output post-processing is specified.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
