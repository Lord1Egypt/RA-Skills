## Description: <br>
一句话说需求，AI 生成完整前后端网站并自动部署到 EdgeOne Pages。支持电商栈（Auth/购物车/支付）、AI 栈（SSE 流式对话）、管理后台。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuboacean](https://clawhub.ai/user/liuboacean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site builders use this skill to scaffold full-stack EdgeOne Pages websites from a short prompt, including e-commerce, AI assistant, and admin-panel variants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated auth, payment, admin, and analytics scaffolding has security-sensitive behavior that may be unsafe before hardening. <br>
Mitigation: Install only in a test or review environment until payment signature verification, fail-closed auth middleware, token handling, secret declarations, privacy controls, migrations, cron jobs, and deployment commands have been manually reviewed and hardened. <br>
Risk: Some generated stacks require sensitive credentials, wallet or payment configuration, OAuth-style tokens, and AI service keys. <br>
Mitigation: Use least-privilege test credentials during review and configure production secrets only after the generated site passes security and privacy review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liuboacean/website-skeleton) <br>
- [README](artifact/README.md) <br>
- [Auth Module Reference](artifact/references/auth-module.md) <br>
- [Payment Module Reference](artifact/references/payment-module.md) <br>
- [AI Chat Module Reference](artifact/references/ai-chat-module.md) <br>
- [Admin Module Reference](artifact/references/admin-module.md) <br>
- [Deployment Reference](artifact/references/deployment.md) <br>
- [Multi-Tenant Reference](artifact/references/multi-tenant.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with generated website files, JavaScript, SQL migrations, JSON templates, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require EdgeOne Pages configuration and secrets for JWT, AI, payment, and database features.] <br>

## Skill Version(s): <br>
3.2.1 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
