## Description:

WebToWork（webto.work）平台 AI 生态能力参考技能包，帮助代理指导或执行 AI 助手挂载、知识库检索增强、模板市场、PWA、APK 打包、网址克隆、AI SEO、多语言、Webhook、会员专区和微信小程序 AI 等平台能力。

This skill is ready for commercial/non-commercial use.

## Publisher:

[slepoh](https://clawhub.ai/user/slepoh)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and site operators use this skill to understand WebToWork capabilities and guide AI-assisted operations through MCP or REST access. It is most useful when users need concise operational guidance for publishing, packaging, cloning, localization, lead review, webhooks, or paid content workflows on WebToWork.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Read-write WebToWork keys can modify or delete platform resources.

Mitigation: Use read-only keys for lookups and reserve read-write keys for narrow, confirmed tasks.

Risk: Publishing, deletion, price changes, webhook configuration, and similar write actions may have business or customer-facing effects.

Mitigation: Confirm the target resource and key parameters with the user before taking these actions.

Risk: HTML submitted for hosting or cloning workflows may contain private or sensitive data.

Mitigation: Review content before submission and avoid sending private data unless the user explicitly approves it.

## Reference(s):

- [WebToWork AI ecosystem reference](references/webto-ai-ecosystem.md)
- [WebToWork OpenAPI specification](https://webto.work/api/v1/openapi.json)
- [ClawHub skill page](https://clawhub.ai/slepoh/skills/webto-ai-ecosystem)
- [ClawHub publisher profile](https://clawhub.ai/user/slepoh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code, shell command, configuration, API, and tool-use snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include instructions for MCP and REST API use, plus confirmations before write actions.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
