## Description:

Manages Supabase migrations, type generation, RLS policies, and edge functions for Supabase-backed Next.js projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guifav](https://clawhub.ai/user/guifav)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, create, apply, and verify Supabase database migrations, RLS policies, generated types, and edge functions in Next.js projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run Supabase CLI database and deployment commands that may use powerful credentials.

Mitigation: Use this only where agents are allowed to change Supabase resources, keep service-role credentials server-side, limit production credentials, and require explicit approval for production pushes or deployments.

Risk: The skill uses unpinned `npx supabase` commands, which can execute a changed CLI version.

Mitigation: Pin the Supabase CLI in the project lockfile and prefer a verified local binary or `npx --no-install`.

Risk: Schema changes can cause data loss when destructive migrations are applied.

Mitigation: Run production dry-runs, prepare backups for destructive changes, and review generated SQL and RLS policies before applying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guifav/skills/supabase-ops)
- [Publisher profile](https://clawhub.ai/user/guifav)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SQL, TypeScript, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce migration files, generated types, edge function code, and verification summaries when applied by an agent.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
