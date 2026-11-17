## Description:

Multi-AI gateway for fullstack apps. Build/deploy websites, React apps, SaaS, ecommerce to Cloudflare Workers. DB (D1/KV/R2), Stripe payments/subscriptions/checkout, auth (login, OAuth, OTP), AI image/audio/video/TTS generation, email, presentations/slides, web scraping/search, CEO interviews/quotes, document parsing/extraction, SMS verification, serverless deploy/API/webhook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renjie-liu](https://clawhub.ai/user/renjie-liu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and builders use this skill to create, deploy, and operate full-stack websites, React apps, SaaS products, ecommerce stores, and AI-enabled workflows. It helps agents call SkillBoss services for model execution, media generation, authentication, payments, storage, search, messaging, document processing, and Cloudflare Worker deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can update and replace local skill files from a remote download.

Mitigation: Prefer manual updates and inspect downloaded files before installing or replacing the local skill.

Risk: The skill can persist API keys and use API credits across local configuration locations.

Mitigation: Use least-privilege or disposable API keys, monitor account balance, and keep credentials out of project build folders and committed files.

Risk: The skill can upload project files and deployment source to external services.

Mitigation: Review project contents before deployment and remove secrets, private data, or files outside the intended release scope.

Risk: The skill may open server-provided URLs through shell commands.

Mitigation: Inspect login, payment, and deployment URLs before opening them, especially in headless or shared environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/renjie-liu/skills/skillboss-3)
- [Publisher Profile](https://clawhub.ai/user/renjie-liu)
- [SkillBoss Website](https://www.skillboss.co)
- [Commands](commands.md)
- [Deployment](deployment.md)
- [API Integration](api-integration.md)
- [Error Handling](error-handling.md)
- [Billing](billing.md)
- [Workflows](workflows.md)
- [Model Reference](reference.md)
- [Remotion Extension Source](https://github.com/remotion-dev/skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, generated project files, configuration examples, and API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify application files, deployment configuration, generated media assets, and API-backed workflow outputs depending on user request.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
