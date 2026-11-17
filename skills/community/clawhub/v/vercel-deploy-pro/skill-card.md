## Description:

Helps agents deploy and update Vercel-hosted sites, including file edits, production deployment, aliasing, and post-deploy verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ranlywood](https://clawhub.ai/user/ranlywood)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide Vercel deployment workflows for web projects, including authentication checks, production deploys, alias handling, and verification of live changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad production deployment actions.

Mitigation: Require an explicit user request, confirm the target project, and review the planned Vercel command before deployment.

Risk: The skill includes guidance for removing Vercel access protections.

Mitigation: Do not remove SSO, password protection, or trusted IP controls unless the user explicitly asks for that exact change and understands protected content may become public.

Risk: Token handling during headless Vercel authentication can expose credentials if handled carelessly.

Mitigation: Use Vercel's normal login flow or a dedicated secrets manager where possible, and keep tokens in session environment variables rather than writing them to files or chat logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ranlywood/skills/vercel-deploy-pro)
- [Publisher profile](https://clawhub.ai/user/ranlywood)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include deployment URLs, Vercel CLI commands, API calls, and verification commands.]

## Skill Version(s):

1.4.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
