## Description:

Generate Supabase API curl commands and SQL query helpers for querying tables, counting rows, inserting records, checking database health, auditing RLS policies, and listing tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate copy-and-run Supabase REST, Management API, and SQL helper commands for projects they control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated commands can run raw SQL or database writes against Supabase projects.

Mitigation: Use the skill only with projects you control and inspect every generated command before running it.

Risk: Untrusted SQL, table names, filters, or JSON values may be embedded into generated shell commands without safe input quoting.

Mitigation: Avoid passing untrusted input and manually quote or rewrite generated commands before execution.

Risk: Powerful Supabase management tokens may be placed directly into shell commands.

Mitigation: Prefer least-privilege credentials and avoid exposing long-lived management tokens in command history or shared logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/loutai0307-prog/skills/supabase-tool)
- [Supabase Project API Settings](https://app.supabase.com/project/YOUR_PROJECT_REF/settings/api)
- [Supabase Account Access Tokens](https://supabase.com/dashboard/account/tokens)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces generated commands for the user to inspect and run; no credentials are stored by the skill.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
