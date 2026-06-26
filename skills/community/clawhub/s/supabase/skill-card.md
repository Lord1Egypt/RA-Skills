## Description: <br>
Connects to Supabase for database operations, storage, SQL queries, table management, and vector similarity search with pgvector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucassynnott](https://clawhub.ai/user/lucassynnott) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to operate Supabase-backed databases from an agent workflow, including querying, CRUD operations, table inspection, RPC calls, and pgvector similarity search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required Supabase credentials can give the agent administrator-level database access. <br>
Mitigation: Install only when administrator-level Supabase access is intended, and prefer a restricted project, restricted key, or test database where possible. <br>
Risk: Write, delete, and raw SQL operations can change or remove database data. <br>
Mitigation: Review every write, delete, and raw SQL action before running it. <br>
Risk: Vector search may send query text to OpenAI for embeddings. <br>
Mitigation: Do not use vector search with sensitive query text unless sending that text to OpenAI is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lucassynnott/supabase) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SUPABASE_URL and SUPABASE_SERVICE_KEY; vector search also requires OPENAI_API_KEY and pgvector setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
