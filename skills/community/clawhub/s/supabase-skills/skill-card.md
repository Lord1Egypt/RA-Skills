## Description:

Manage Volcengine Supabase workspaces, branches, SQL queries, migrations, Edge Functions, Storage, and TypeScript type generation through a local CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techstylex](https://clawhub.ai/user/techstylex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and manage Volcengine Supabase workspaces, branches, database SQL and migrations, Edge Functions, storage buckets, and generated TypeScript types from an agent conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags credential and production-data risk from an unsafe HTTP default and real administrative operations.

Mitigation: Use least-privilege Volcengine credentials, set SUPABASE_ENDPOINT_SCHEME=https, and test destructive operations on an isolated branch before touching production resources.

Risk: The security review says the READ_ONLY guard should not be relied on to prevent SQL changes.

Mitigation: Treat READ_ONLY as advisory only and review SQL, migration, branch reset, delete, deploy, and key-reveal commands before execution.

Risk: The skill can reveal Supabase keys when get-keys is run with --reveal.

Mitigation: Avoid get-keys --reveal unless deliberately handling secrets, and keep any revealed service-role credentials out of client-side code and logs.

## Reference(s):

- [Volcengine](https://www.volcengine.com/)
- [Tool Reference](references/tool-reference.md)
- [Workflows](references/workflows.md)
- [SQL Playbook](references/sql-playbook.md)
- [Application Integration Guide](references/app-integration-guide.md)
- [Schema Guide](references/schema-guide.md)
- [RLS Guide](references/rls-guide.md)
- [Edge Function Development Guide](references/edge-function-dev-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, code snippets, and JSON or text command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute local CLI commands against Volcengine Supabase when configured with credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
