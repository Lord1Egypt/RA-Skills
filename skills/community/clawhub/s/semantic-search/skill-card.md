## Description: <br>
Semantic Search provides enterprise semantic search over database tables, fields, and files, and can generate SQL from natural-language questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sevenal](https://clawhub.ai/user/Sevenal) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and data teams use this skill to let agents find relevant database schema, fields, and files, then produce SQL-backed answers from natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live database data and may send schema or query context to model and reranking services. <br>
Mitigation: Install only in controlled environments with read-only database credentials, approved data, approved private or model endpoints, and reviewed logging and retention settings. <br>
Risk: Bundled examples include unsafe configuration patterns such as insecure database transport and placeholder or exposed credentials. <br>
Mitigation: Remove or rotate any credentials shown in documentation, store secrets outside the artifact, and disable insecure transport for production use. <br>
Risk: Text-to-SQL output can produce incorrect, overly broad, or sensitive database queries. <br>
Mitigation: Review generated SQL before execution, restrict database privileges and resource scopes, and prefer non-production data for validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sevenal/semantic-search) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Sevenal) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration] <br>
**Output Format:** [JSON responses containing search results, generated SQL, and data payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports table_search, field_search, file_search, and data_gen actions with caller-supplied query, resource, and limit parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
