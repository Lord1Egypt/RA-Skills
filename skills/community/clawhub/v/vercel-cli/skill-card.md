## Description:

Vercel CLI skill for deploying and managing Vercel projects from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an agent propose Vercel CLI commands for deploying projects, managing deployments, configuring domains and SSL certificates, handling environment variables, and checking account or team state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact production deployment, promotion, rollback, deletion, raw API, purchase, domain, and secret-management workflows.

Mitigation: Use a least-privilege Vercel token and require explicit approval before production, promotion, rollback, removal, purchase, raw API, or domain-change commands.

Risk: Pulled environment files and authentication tokens may expose secrets if logged, passed on command lines, or committed.

Mitigation: Prefer VERCEL_TOKEN over command-line token flags and keep pulled .env files local, gitignored, and out of logs.

## Reference(s):

- [ClawHub Vercel CLI Skill Page](https://clawhub.ai/openlark/skills/vercel-cli)
- [Vercel Account Tokens](https://vercel.com/account/tokens)
- [Vercel CLI Command Reference](references/commands.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include deployment, rollback, domain, environment variable, and account-management command proposals that should be reviewed before execution.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
