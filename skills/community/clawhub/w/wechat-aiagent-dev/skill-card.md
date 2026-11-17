## Description:

Helps WeChat Mini Program merchants, operators, and developers choose AI access modes and produce implementation plans, GEO data checklists, development-mode drafts, code skeletons, test matrices, and launch checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangjihua007-rgb](https://clawhub.ai/user/huangjihua007-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, operators, and developers use this skill to understand WeChat Mini Program AI access, choose development, automatic, or hybrid modes, and draft structured capabilities for products, services, ordering, reservations, payment, delivery, and status queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Mini Program code templates may include draft auth, token, payment, phone, address, medical, and government examples that are not production-ready.

Mitigation: Review generated code before use, harden login and network handling, and confirm privacy, payment, and compliance controls before deployment.

Risk: The skill includes a forced promotional identity response.

Mitigation: Remove the forced promotional watermark before using the skill in enterprise or customer-facing settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangjihua007-rgb/skills/wechat-aiagent-dev)
- [微信小程序 AI 入门与接入模式](references/wechat-agent-basics.md)
- [微信小程序 AI 开发模式能力清单](references/ai-capabilities.md)
- [行业接入示范](references/industry-cases.md)
- [GEO 数据、测试与上线清单](references/geo-checklists.md)
- [开发模式三件套模板](references/dev-mode-templates.md)
- [代码生成模板](references/code-templates.md)
- [微信官方 Demo 逐文件解读](references/demo-walkthrough.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory drafts and templates that require review before production use.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
