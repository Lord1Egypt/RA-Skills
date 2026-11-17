## Description:

Manage Zilliz Cloud vector databases through zilliz-cli, including setup, clusters, collections, indexes, partitions, databases, vectors, RBAC, backups, imports, billing, monitoring, projects, and regions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanshuyou](https://clawhub.ai/user/zhanshuyou)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and engineers use this skill to operate Zilliz Cloud vector database resources through zilliz-cli. It helps agents propose setup, status, data-plane, control-plane, RBAC, backup, import, billing, monitoring, project, and region commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect real Zilliz Cloud resources, including deleting or dropping clusters, collections, databases, backups, users, roles, partitions, indexes, volumes, and billing-related state.

Mitigation: Use least-privilege Zilliz credentials and require explicit user confirmation before every delete, drop, RBAC, billing, restore, suspend, or otherwise irreversible action.

Risk: Credential and payment-card command examples could expose API keys, passwords, or card details if entered in chat or run inside an agent-controlled shell.

Mitigation: Keep authentication, configuration, password updates, and card binding in the user's own terminal; never request secrets in chat or echo them into logs.

Risk: Installing or upgrading zilliz-cli without version pinning can change CLI behavior or dependencies between runs.

Mitigation: Prefer a pinned or isolated zilliz-cli installation for production use and verify the CLI version before running operational commands.

## Reference(s):

- [Setup and authentication](references/setup.md)
- [Clusters](references/cluster.md)
- [Collections](references/collection.md)
- [Vector operations](references/vector.md)
- [Indexes](references/index.md)
- [Databases](references/database.md)
- [Partitions](references/partition.md)
- [Users and roles](references/user-role.md)
- [Backups](references/backup.md)
- [Import](references/import.md)
- [Billing](references/billing.md)
- [Monitoring](references/monitoring.md)
- [Projects and regions](references/project-region.md)
- [Zilliz](https://zilliz.com/)
- [Zilliz Cloud](https://cloud.zilliz.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend JSON output for programmatic CLI parsing; destructive and sensitive operations require explicit confirmation or user-side terminal entry.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
