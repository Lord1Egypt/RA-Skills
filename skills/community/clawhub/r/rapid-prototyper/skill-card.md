## Description:

Helps agents rapidly build proof-of-concept web apps, prototypes, and MVPs using a Next.js 14, Supabase, Clerk, shadcn/ui, and Prisma stack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bullkis1](https://clawhub.ai/user/bullkis1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold and ship fast MVPs or proof-of-concept web applications, focusing on a single core user flow, feedback collection, and deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest unpinned package scaffolding and dependency installs.

Mitigation: Pin package and CLI versions, review generated code, and inspect lockfiles before use.

Risk: The skill may configure external services and push schema changes.

Mitigation: Use non-production service projects while prototyping and review schema changes before applying them to shared or production databases.

Risk: The skill may deploy prototypes publicly or to production targets.

Mitigation: Confirm the deployment target and environment variables before publishing, and prefer preview deployments until the application has been reviewed.

Risk: The skill encourages feedback collection that can capture user data.

Mitigation: Add privacy safeguards, data minimization, server-side validation, and storage controls before collecting feedback from real users.

## Reference(s):

- [Stack Setup Reference](references/stack-setup.md)
- [Common Patterns](references/patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/bullkis1/skills/rapid-prototyper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scaffold commands, application code patterns, environment variable guidance, deployment steps, and implementation recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
