## Description: <br>
Manage Supabase projects from the command line by querying tables, changing rows, managing RLS policies, handling auth users, and working with storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vanthienha199](https://clawhub.ai/user/vanthienha199) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and modify Supabase project data, policies, auth users, and storage through REST API calls and formatted Markdown results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate on live Supabase databases, including inserts, updates, deletes, schema changes, and raw SQL or RPC execution. <br>
Mitigation: Review before installing, use a test Supabase project first, and require explicit confirmation before any insert, update, delete, schema change, or raw SQL execution. <br>
Risk: Supabase access can be over-scoped or exposed if credentials are handled loosely. <br>
Mitigation: Use restricted anon keys protected by Row Level Security, provide credentials through environment variables, and do not use service-role keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vanthienha199/supabase-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and formatted Markdown tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SUPABASE_URL and SUPABASE_ANON_KEY; requests confirmation before update or delete operations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
