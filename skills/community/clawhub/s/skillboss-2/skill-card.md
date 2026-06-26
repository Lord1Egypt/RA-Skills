## Description: <br>
Skillboss helps agents use SkillBoss services to build and deploy full-stack apps, integrate AI generation, payments, authentication, messaging, document processing, web search, and Cloudflare Worker workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yshuolu](https://clawhub.ai/user/yshuolu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Skillboss to add AI content generation, API integrations, authentication, payments, messaging, and deployment workflows to full-stack web apps. The skill is also used to guide Cloudflare Worker, Stripe, e-commerce, Remotion, and content-generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts, files, documents, phone numbers, email recipients, deployment source, and configuration to SkillBoss or HeyBoss services. <br>
Mitigation: Install and use it only when you trust those services with that data, and minimize sensitive inputs before running API or deployment commands. <br>
Risk: Deployment workflows can upload environment data and deploy code. <br>
Mitigation: Remove secrets from .env and wrangler.toml vars unless intentionally required, and review generated code and deployment commands before execution. <br>
Risk: API keys may be stored in local credentials or skill configuration files. <br>
Mitigation: Treat the API key as a server-side secret and avoid committing config.json or local credential files. <br>
Risk: Messaging, email, payment, and Stripe workflows can have external side effects. <br>
Mitigation: Confirm recipients, phone numbers, payment setup, and account actions before running the related commands. <br>
Risk: The skill documentation describes update behavior that can run local update scripts after an API response requests it. <br>
Mitigation: Review any update prompt and local update script before allowing it to run. <br>


## Reference(s): <br>
- [ClawHub Skillboss release page](https://clawhub.ai/yshuolu/skillboss-2) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Commands reference](artifact/commands.md) <br>
- [API integration guide](artifact/api-integration.md) <br>
- [Deployment guide](artifact/deployment.md) <br>
- [Workflow guides](artifact/workflows.md) <br>
- [Remotion extension guide](artifact/extensions/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON and TypeScript examples, and generated project or deployment artifacts when commands are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can trigger external API calls, content generation, messaging, payment setup, and deployments when the agent runs the documented commands.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
