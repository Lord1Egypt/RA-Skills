## Description:

Create ephemeral TiDB Cloud Zero databases for agent workflows in Technical Preview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bosn](https://clawhub.ai/user/bosn)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to provision disposable TiDB Cloud Zero databases, run SQL smoke tests, and connect through MySQL-compatible clients for short-lived workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Temporary database connection details include credentials that can be exposed if saved insecurely or committed.

Mitigation: Store response files with restrictive permissions, avoid committing them, delete them when done, and prefer safer MySQL credential handling over passwords in commands.

Risk: The TiDB Cloud Zero API is described as Technical Preview and the current API path may change.

Mitigation: Confirm the current TiDB Cloud Zero endpoint and response shape before relying on the skill in repeatable workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bosn/skills/zero)
- [TiDB SQL skill](https://skills.sh/pingcap/agent-rules/tidb-sql)
- [PyTiDB skill](https://skills.sh/pingcap/agent-rules/pytidb)
- [TiDB Cloud docs](https://docs.pingcap.com/tidbcloud/)
- [TiDB Cloud website](https://tidbcloud.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, SQL, JSON, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include temporary database connection details that should be treated as secrets.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
