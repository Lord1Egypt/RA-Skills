## Description:

Supabase integration for Hakke Studio projects covering authentication, database operations, storage, edge functions, and Vercel deployment support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[studio-hakke](https://clawhub.ai/user/studio-hakke)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to configure Supabase for Hakke Studio and multi-tenant Next.js SaaS projects, including auth, RLS policies, storage, edge functions, environment variables, and deployment setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes an example admin-user SQL statement with a hardcoded password.

Mitigation: Do not copy the sample password into any real Supabase project; use a secure user-provisioning flow and project-specific credentials.

Risk: The skill references SUPABASE_SERVICE_ROLE_KEY, which is privileged secret material.

Mitigation: Keep the service role key backend-only, store it in managed secret storage, and never expose it to browsers or committed files.

Risk: Database reset and SECURITY DEFINER SQL examples can affect tenant isolation or production data if used without review.

Mitigation: Restrict reset commands to development environments and review SECURITY DEFINER functions, permissions, and tenant checks before deployment.

Risk: The Supabase CLI installation example does not pin or verify the installed package.

Mitigation: Pin or verify CLI installation before use in production or CI workflows.

## Reference(s):

- [Supabase Docs](https://supabase.com/docs)
- [Supabase Dashboard](https://supabase.com/dashboard)
- [Supabase CLI Reference](https://supabase.com/docs/reference/cli)
- [ClawHub Skill Page](https://clawhub.ai/studio-hakke/skills/supabase-hakke)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL, TypeScript, environment variable, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational guidance for Supabase CLI, RLS policies, storage, edge functions, and Vercel environment configuration.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
