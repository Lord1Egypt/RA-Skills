## Description:

Migrate Next.js projects from Vercel to Cloudflare Workers with Supabase and Hyperdrive support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiafar](https://clawhub.ai/user/jiafar)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to assess and migrate Next.js and Supabase applications from Vercel to Cloudflare Workers, including Hyperdrive connection setup and environment-variable refactoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package-install and Wrangler setup commands can modify dependencies, lockfiles, and deployment configuration.

Mitigation: Pin @opennextjs/cloudflare and wrangler versions where practical, review dependency and lockfile changes, and test deployment configuration before release.

Risk: Database connection strings or passwords may be exposed if copied directly into reusable shell history or shared configuration.

Mitigation: Use local secret files or secret-management workflows for credentials, and avoid pasting real database passwords into reusable shell commands.

Risk: The skill references a migration script that is not present in the artifact.

Mitigation: Treat automated migration instructions as guidance unless a reviewed migration script is supplied, and manually inspect code changes before applying them.

## Reference(s):

- [Environment Variable Patterns on Cloudflare Workers](references/env-patterns.md)
- [Hyperdrive + Supabase Setup Guide](references/hyperdrive-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included analysis script emits a console migration-readiness report for a supplied project path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
