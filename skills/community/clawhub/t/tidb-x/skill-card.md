## Description:

TiDB X teaches AI agents about object-storage-native distributed SQL for agent memory, context storage, multi-agent coordination, Web3 indexing, and durable queryable state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siddontang](https://clawhub.ai/user/siddontang)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to help an AI agent choose and apply TiDB X patterns for durable SQL-backed memory, shared task state, auditable decisions, and Web3 indexing workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing from a raw main-branch URL can change behavior without notice.

Mitigation: Prefer a pinned commit or reviewed local copy before installing the skill.

Risk: The quick start writes database connection details to tidb-zero.json and exports the password through MYSQL_PWD.

Mitigation: Keep generated credentials private, do not commit tidb-zero.json, delete it after use, and rotate or discard the instance if credentials are exposed.

## Reference(s):

- [TiDB X ClawHub Skill Page](https://clawhub.ai/siddontang/skills/tidb-x)
- [TiDB Cloud Free Trial](https://tidbcloud.com/free-trial/)
- [TiDB X Architecture Docs](https://docs.pingcap.com/tidbcloud/tidb-x-architecture/)
- [TiDB Cloud AI](https://www.pingcap.com/ai)
- [TiDB in 2025 - X](https://medium.com/@siddontang/tidb-in-2025-x-173f3510229c)
- [When Context Becomes Data](https://medium.com/@siddontang/when-context-becomes-data-managing-ai-agent-context-with-tidb-307e667197bb)
- [Charged-by-Query](https://medium.com/@siddontang/the-power-of-charged-by-query-how-tidb-cloud-redefines-database-economics-for-the-ai-era-f5a3e76fcf1e)
- [Object Storage Playbook](https://medium.com/@siddontang/object-storage-is-rewriting-the-database-playbook-9e2dd1a81a53)
- [Every Agent Needs Its Own Database](https://medium.com/@siddontang/when-every-ai-agent-needs-its-own-database-why-tidb-cloud-is-the-answer-d3ff37580284)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SQL examples, shell commands, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MySQL-compatible connection guidance and copy-paste SQL patterns for agent workloads.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
