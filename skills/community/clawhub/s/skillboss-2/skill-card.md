## Description:

Multi-AI gateway for fullstack apps. Build/deploy websites, React apps, SaaS, ecommerce to Cloudflare Workers. DB (D1/KV/R2), Stripe payments/subscriptions/checkout, auth (login, OAuth, OTP), AI image/audio/video/TTS generation, email, presentations/slides, web scraping/search, CEO interviews/quotes, document parsing/extraction, SMS verification, serverless deploy/API/webhook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yshuolu](https://clawhub.ai/user/yshuolu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and builders use this skill to add AI generation, search, document processing, messaging, authentication, payments, and Cloudflare Worker deployment workflows to full-stack applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, files, deployment bundles, emails or SMS requests, product changes, and payment setup requests may be sent to SkillBoss or HeyBoss services.

Mitigation: Use the skill only for projects and recipients the user explicitly intends to modify or contact, and avoid submitting sensitive data unless the service use is acceptable.

Risk: Credential persistence can expose API keys if they are copied into client-side code or committed to public repositories.

Mitigation: Keep API keys in local credential storage or server-side configuration, and review generated code before publishing.

Risk: The security summary notes an automatic updater path that can run an uninspected shell script.

Mitigation: Review any update script before executing it and avoid automatic updates in environments where shell-script changes require approval.

Risk: Deployment, product, payment, email, and SMS commands can make externally visible changes.

Mitigation: Confirm target project, account, payment setup, recipient lists, and deployment destination before running those commands.

## Reference(s):

- [SkillBoss ClawHub release](https://clawhub.ai/yshuolu/skills/skillboss-2)
- [SkillBoss website](https://www.skillboss.co)
- [API Integration](api-integration.md)
- [Commands Reference](commands.md)
- [Deployment](deployment.md)
- [Workflows](workflows.md)
- [SkillBoss Reference](reference.md)
- [Error Handling](error-handling.md)
- [Billing](billing.md)
- [Remotion Best Practices Extension](extensions/remotion/EXTENSION_SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, JSON responses, generated files, and application code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated media, deployment artifacts, credentials, and project configuration files when the user invokes those workflows.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
