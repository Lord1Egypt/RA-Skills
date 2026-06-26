## Description: <br>
Supabase integration for Hakke Studio projects, covering auth, database, storage, edge functions, and Vercel-backed full-stack deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[studio-hakke](https://clawhub.ai/user/studio-hakke) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers working on Hakke Studio Supabase projects use this skill for setup and operational guidance around auth, database migrations, RLS policies, storage, edge functions, environment variables, and Vercel deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Supabase admin commands can affect the wrong project if the active project is not checked first. <br>
Mitigation: Verify the active Supabase project before running migrations or administrative commands. <br>
Risk: Database reset commands can destroy production data. <br>
Mitigation: Never run `supabase db reset` on production. <br>
Risk: The Supabase service role key grants elevated access if exposed to clients or logs. <br>
Mitigation: Keep `SUPABASE_SERVICE_ROLE_KEY` server-side in protected secrets. <br>
Risk: The example server client is not sufficient for authenticated RLS behavior in production. <br>
Mitigation: Replace the example with a cookie-aware Supabase SSR client before relying on authenticated RLS behavior. <br>


## Reference(s): <br>
- [Supabase Docs](https://supabase.com/docs) <br>
- [Supabase CLI Reference](https://supabase.com/docs/reference/cli) <br>
- [Supabase Dashboard](https://supabase.com/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, SQL, and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes project-specific Supabase and Vercel operational examples; commands require human review before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence release and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
