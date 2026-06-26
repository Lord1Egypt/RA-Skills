## Description: <br>
Supabase API integration with managed authentication for database tables, auth users, and storage buckets through Maton. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect and operate connected Supabase projects, including PostgREST table access, auth user management, and storage bucket operations. It is intended for Supabase workflows that need managed Maton authentication through MATON_API_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change data in a connected Supabase project through Maton. <br>
Mitigation: Install only if Maton is trusted with the project and prefer staging or least-privileged projects for exploration. <br>
Risk: POST, PUT, PATCH, and DELETE operations can modify production data, auth users, or storage resources. <br>
Mitigation: Review the target resource, filters, and intended effect before approving any write operation. <br>
Risk: When multiple Supabase connections exist, requests may target the wrong project if the connection is ambiguous. <br>
Mitigation: Specify the intended connection explicitly before executing project-specific requests. <br>


## Reference(s): <br>
- [Maton](https://maton.ai) <br>
- [Supabase REST API Guide](https://supabase.com/docs/guides/api) <br>
- [PostgREST Documentation](https://postgrest.org/en/stable/) <br>
- [Supabase Auth API](https://supabase.com/docs/reference/javascript/auth-api) <br>
- [Supabase Storage API](https://supabase.com/docs/reference/javascript/storage-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP endpoint descriptions and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; API operations act through Maton against the selected connected Supabase project.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
