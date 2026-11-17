## Description:

Provision a disposable MySQL-compatible database instantly for free, no auth required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoubingwu](https://clawhub.ai/user/zoubingwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create temporary MySQL-compatible TiDB Cloud Zero databases for application prototyping, testing, and AI-augmented SQL workflows. It also guides users on TLS connections, short-lived credentials, and claiming an instance before expiration when persistence is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional BYOK embedding examples may expose OpenAI, Cohere, or other provider API keys if pasted into disposable or untrusted database sessions.

Mitigation: Use test-scoped or short-lived keys, avoid shared databases for long-lived credentials, and rotate keys if they were exposed.

Risk: Zero instances are temporary and are destroyed at expiration if not claimed.

Mitigation: Use the claim URL before the expiration timestamp when persistence is required, and treat generated database credentials as short-lived.

Risk: Connection details can leak through shell history or process listings when passwords are passed directly as command arguments.

Mitigation: Prefer environment variables such as MYSQL_PWD and require TLS for client and driver connections.

## Reference(s):

- [TiDB Cloud Zero Homepage](https://zero.tidbcloud.com/)
- [TiDB AI SQL Quickstart](https://docs.pingcap.com/ai/quickstart-via-sql/)
- [TiDB AI Auto Embedding Overview](https://docs.pingcap.com/ai/vector-search-auto-embedding-overview/)
- [TiDB Cloud Documentation](https://docs.pingcap.com/tidbcloud/)
- [TiDB Vector Search Data Types](https://docs.pingcap.com/ai/vector-search-data-types/)
- [TiDB Vector Search Functions and Operators](https://docs.pingcap.com/ai/vector-search-functions-and-operators/)
- [TiDB Vector Search Index](https://docs.pingcap.com/ai/vector-search-index/)
- [TiDB Cloud Vector Search Limitations](https://docs.pingcap.com/tidbcloud/vector-search-limitations/)
- [Vector Reference](references/vector.md)
- [Auto Embedding Reference](references/auto-embedding.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, SQL, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include temporary database credentials, connection strings, claim URLs, SQL examples, and TLS configuration notes.]

## Skill Version(s):

1.3.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
