## Description:

Scaffolds full-stack EdgeOne Pages websites from a short prompt, including reusable e-commerce, AI chat, admin, multi-tenant, SEO, analytics, and deployment assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuboacean](https://clawhub.ai/user/liuboacean)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site builders use this skill to generate an EdgeOne Pages website skeleton with front-end pages, edge and cloud functions, database migrations, templates, and deployment guidance for e-commerce, AI assistant, or SaaS admin scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled auth, database, payment, and analytics code may put deployed users or transactions at risk.

Mitigation: Review and fix the auth flow, token responses, cookie flags, D1 async handling, payment transaction behavior, and analytics opt-out or feature gating before using real users, production databases, or payment credentials.

Risk: The server security verdict is suspicious and marks the skill as review-required before real-site use.

Mitigation: Run security review and tests before installation or deployment, and keep credentials and production data disconnected until the review is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuboacean/skills/website-skeleton)
- [README](README.md)
- [Auth module](references/auth-module.md)
- [Payment module](references/payment-module.md)
- [AI chat module](references/ai-chat-module.md)
- [Admin module](references/admin-module.md)
- [Multi-tenant module](references/multi-tenant.md)
- [Edge functions](references/edge-functions.md)
- [Cloud functions](references/cloud-functions.md)
- [KV storage](references/kv-storage.md)
- [Middleware](references/middleware.md)
- [Deployment](references/deployment.md)
- [Integration tests](references/integration-tests.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with generated project files, JSON templates, JavaScript modules, SQL migrations, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a scaffold intended for review, configuration, testing, and deployment through EdgeOne Pages.]

## Skill Version(s):

3.2.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
