## Description: <br>
Provision a disposable MySQL-compatible database instantly for free, no auth required. Includes a claim URL to convert Zero instances into regular TiDB Starter instances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoubingwu](https://clawhub.ai/user/zoubingwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create short-lived TiDB Cloud Zero databases for prototyping, testing, and AI-assisted SQL or vector search workflows. It also guides users on claiming an instance before expiration when persistence is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Temporary database connection strings include credentials that can grant access to the disposable instance. <br>
Mitigation: Keep generated connection strings private, prefer environment variables over command-line password arguments, and treat credentials as short-lived secrets. <br>
Risk: Connections made without TLS can expose database traffic or credentials in transit. <br>
Mitigation: Use TLS for every client connection, such as `--ssl-mode=REQUIRED` for mysql CLI or `ssl: true` for drivers. <br>
Risk: Unclaimed Zero instances expire and are destroyed, so data can be lost. <br>
Mitigation: Avoid storing sensitive production data in disposable instances and open the claim URL before `expiresAt` when persistence is required. <br>
Risk: Optional BYOK embedding examples may involve third-party provider API keys. <br>
Mitigation: Use restricted or temporary provider keys and avoid exposing them in shared SQL, logs, or transcripts. <br>


## Reference(s): <br>
- [TiDB Cloud Zero homepage](https://zero.tidbcloud.com/) <br>
- [TiDB Cloud Zero instance API](https://zero.tidbapi.com/v1beta1/instances) <br>
- [TiDB Cloud docs](https://docs.pingcap.com/tidbcloud/) <br>
- [TiDB AI SQL quickstart](https://docs.pingcap.com/ai/quickstart-via-sql/) <br>
- [TiDB Auto Embedding overview](https://docs.pingcap.com/ai/vector-search-auto-embedding-overview/) <br>
- [TiDB Vector Search](references/vector.md) <br>
- [TiDB Auto Embedding](references/auto-embedding.md) <br>
- [ClawHub release page](https://clawhub.ai/zoubingwu/tidb-cloud-zero) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON, SQL, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include temporary database connection details, claim URL guidance, TLS connection settings, and SQL examples for vector search or auto embedding.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
