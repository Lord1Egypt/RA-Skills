## Description: <br>
Manage Volcengine Supabase workspaces, branches, SQL queries, migrations, Edge Functions, Storage, and TypeScript type generation via a local CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TechStylex](https://clawhub.ai/user/TechStylex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to administer Volcengine Supabase resources, inspect workspaces and branches, run SQL and migrations, deploy Edge Functions, manage Storage, and generate TypeScript types from an agent conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer real Volcengine Supabase resources, including database, branch, deployment, storage, and secret-access operations. <br>
Mitigation: Use a non-production workspace or branch first, set READ_ONLY=true for exploration, and review planned changes before allowing write operations. <br>
Risk: SQL execution and migrations can change or destroy data if the query is incorrect. <br>
Mitigation: Prefer read-only inspection before changes, review execute-sql queries manually, and apply reviewed migration files for schema changes. <br>
Risk: get-keys --reveal can expose credentials and service keys. <br>
Mitigation: Avoid revealing keys unless necessary, treat revealed values as secrets, and keep service-role keys out of client-side code and logs. <br>
Risk: The release depends on a pinned GitHub SDK dependency. <br>
Mitigation: Review the pinned dependency before using production credentials or production workspaces. <br>


## Reference(s): <br>
- [Volcengine](https://www.volcengine.com/) <br>
- [Tool Reference](references/tool-reference.md) <br>
- [Workflows](references/workflows.md) <br>
- [SQL Playbook](references/sql-playbook.md) <br>
- [Application Integration Guide](references/app-integration-guide.md) <br>
- [Database Schema Design and Migration Guide](references/schema-guide.md) <br>
- [Row Level Security Strategy Guide](references/rls-guide.md) <br>
- [Edge Function Development Guide](references/edge-function-dev-guide.md) <br>
- [Pinned Volcengine Python SDK Dependency](https://github.com/sjcsjcsjc/volcengine-python-sdk.git@9905a8853a0e5fd26fdae93eefb4f201e8bef539) <br>
- [ClawHub Skill Page](https://clawhub.ai/TechStylex/supabase-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell, SQL, TypeScript, Python, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command results, resource identifiers, and secret-redacted configuration details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
