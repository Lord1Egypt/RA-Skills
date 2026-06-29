## Description: <br>
Manage Volcengine AI Native BaaS for Supabase (AIDAP) database workspaces as a deployment database provider for setup, branch management, connection details, SQL, migrations, Edge Functions, Storage, and TypeScript type generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and deployment engineers use this skill to provision and operate Volcengine AIDAP Supabase or PostgreSQL workspaces, retrieve deployment connection settings, and apply database, storage, and Edge Function workflows. It is intended for real cloud and database resources, so users should start in non-production workspaces and confirm destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through high-privilege Volcengine Supabase and PostgreSQL operations, including database changes and resource deletion. <br>
Mitigation: Use non-production workspaces first, require explicit user confirmation before migrations or deletes, and set READ_ONLY=true for inspection-only data-plane work. <br>
Risk: Service-role keys and database URLs provide broad access if exposed in logs, frontend code, or final responses. <br>
Mitigation: Store credentials in local files with restrictive permissions, avoid printing secrets, and summarize only resource IDs, host details, verification results, and credential file paths. <br>
Risk: One command labeled as a read path can still alter the target database according to the security review. <br>
Mitigation: Treat all database-interacting commands as potentially state-changing, review the exact command and target workspace before execution, and prefer READ_ONLY=true unless a write is intended. <br>


## Reference(s): <br>
- [CLI action map and bootstrap notes](references/tool-reference.md) <br>
- [Application integration patterns](references/app-integration-guide.md) <br>
- [Schema and RLS guidance](references/schema-rls-guide.md) <br>
- [SQL playbook](references/sql-playbook.md) <br>
- [Edge Function development](references/edge-function-dev-guide.md) <br>
- [Deployment database-provider wiring](references/deploy-provider.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline shell, SQL, JSON, Python, and TypeScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local environment files and generated TypeScript types when users ask for those workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
