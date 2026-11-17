## Description:

Connect to Supabase for database operations, vector search, and storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucassynnott](https://clawhub.ai/user/lucassynnott)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to let an agent run Supabase database queries, table operations, RPC calls, storage-adjacent workflows, and pgvector similarity search against an authorized Supabase project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate with a Supabase service role key that may grant full database authority.

Mitigation: Install only for projects where agent-level full database access is acceptable, and prefer a restricted credential or isolated Supabase project when possible.

Risk: Raw SQL, update, and delete actions can modify or remove production data.

Mitigation: Double-check every raw SQL, update, and delete request before execution, especially when filters or table names are agent-proposed.

Risk: Vector-search queries may send sensitive text to an embedding provider when embeddings are generated externally.

Mitigation: Avoid vector-search queries containing sensitive text unless sending that text to the configured embedding provider is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lucassynnott/skills/supabase)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, SQL examples, JSON payloads, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SUPABASE_URL and SUPABASE_SERVICE_KEY; OPENAI_API_KEY may be used for embedding-backed vector search.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
