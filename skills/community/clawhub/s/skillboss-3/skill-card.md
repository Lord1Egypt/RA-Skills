## Description: <br>
Multi-AI gateway for fullstack apps. Build/deploy websites, React apps, SaaS, ecommerce to Cloudflare Workers. DB (D1/KV/R2), Stripe payments/subscriptions/checkout, auth (login, OAuth, OTP), AI image/audio/video/TTS generation, email, presentations/slides, web scraping/search, CEO interviews/quotes, document parsing/extraction, SMS verification, serverless deploy/API/webhook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renjie-liu](https://clawhub.ai/user/renjie-liu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to build, deploy, and operate full-stack applications with SkillBoss services for AI model access, Cloudflare Worker deployment, databases, payments, authentication, messaging, document processing, and media generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform broad AI, deployment, credential, upload, payment, SMS, email, and authentication workflows through SkillBoss and HeyBoss services. <br>
Mitigation: Install only if the user trusts SkillBoss/HeyBoss with the data and actions involved, and use test recipients, test accounts, and non-production Stripe and deployment settings before production use. <br>
Risk: The security evidence flags silent self-updating behavior as a review concern. <br>
Mitigation: Review or disable the self-update flow before installation, and inspect update output before re-running interrupted commands. <br>
Risk: Credential and project configuration handling may expose real secrets if used carelessly. <br>
Mitigation: Prefer environment variables or trusted credential stores, avoid placing real secrets in project config or Wrangler variables, and rotate any exposed keys. <br>
Risk: The security evidence says the auth template should be fixed before production use. <br>
Mitigation: Review and repair authentication templates before using them for public or production applications. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/renjie-liu/skillboss-3) <br>
- [SkillBoss Website](https://www.skillboss.co/) <br>
- [Commands](commands.md) <br>
- [Deployment](deployment.md) <br>
- [API Integration](api-integration.md) <br>
- [Error Handling](error-handling.md) <br>
- [Billing](billing.md) <br>
- [Workflows](workflows.md) <br>
- [Model Reference](reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, configuration files, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke SkillBoss and HeyBoss APIs, write application artifacts, configure credentials, and deploy projects when used by an agent.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
