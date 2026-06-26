## Description: <br>
Documents the tool services in Teamgram Server including idgen (Snowflake ID), status (online TTL), dfs (Minio file storage), and media (metadata/thumbnails). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhihang9978](https://clawhub.ai/user/zhihang9978) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers maintaining Teamgram Server use this skill to understand the idgen, status, dfs, and media services, including their configuration snippets, service dependencies, and code paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Development-oriented service configuration examples may be reused without hardening, including exposed HTTP listeners or default database connection strings. <br>
Mitigation: Review listener bindings, credentials, and database or storage settings before adapting the examples outside local development. <br>


## Reference(s): <br>
- [Teamgram Server Repository](https://github.com/teamgram/teamgram-server) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown with YAML and text configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no executable output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
