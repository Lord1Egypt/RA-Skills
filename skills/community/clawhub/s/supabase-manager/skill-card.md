## Description:

Manage Supabase projects from the command line, including querying tables, changing rows, managing RLS policies, handling auth users, and working with storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vanthienha199](https://clawhub.ai/user/vanthienha199)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect and operate Supabase projects through REST API calls, including table queries, row mutations, auth-user work, storage operations, and RLS-related tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify remote Supabase data through generated REST and RPC shell commands.

Mitigation: Require explicit approval for state-changing operations, confirm the Supabase URL, and review table names, filters, and payloads before execution.

Risk: Credential handling or over-privileged keys could expose data beyond the intended RLS boundary.

Mitigation: Use only the Supabase anon key, never provide a service-role key, rely on RLS policies, and store credentials only in a secure credential store.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vanthienha199/skills/supabase-manager)
- [Publisher profile](https://clawhub.ai/user/vanthienha199)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with formatted tables and inline bash/curl command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SUPABASE_URL and SUPABASE_ANON_KEY; query results over 50 rows are summarized by showing the first 20 rows.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
