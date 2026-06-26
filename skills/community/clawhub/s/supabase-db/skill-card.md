## Description: <br>
Connect to Supabase for SQL queries, CRUD, table management, and vector similarity search using pgvector and OpenAI embeddings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvanhorn](https://clawhub.ai/user/mvanhorn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to inspect and operate Supabase Postgres projects, including SQL queries, CRUD operations, table and schema review, RPC calls, and pgvector similarity search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad database write, delete, RPC, and raw SQL authority through privileged Supabase credentials. <br>
Mitigation: Use a staging project or narrowly scoped credential where possible, keep backups, and require human review before SQL, update, delete, or RPC actions. <br>
Risk: Supabase keys and database content may be exposed through logs or untrusted prompts. <br>
Mitigation: Protect Supabase credentials from logs and prompts, and avoid running the skill in sessions that include untrusted instructions. <br>
Risk: Vector search may send query text to OpenAI for embeddings. <br>
Mitigation: Avoid vector search for confidential query text unless sending that text to OpenAI is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mvanhorn/supabase-db) <br>
- [Supabase](https://supabase.com) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; command responses are JSON when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Supabase project credentials; vector search can use OpenAI embeddings.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
