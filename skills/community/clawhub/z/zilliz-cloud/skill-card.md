## Description:

Manage Zilliz Cloud clusters and Milvus vector databases - cluster ops, collections, vector search, RBAC, backups, imports, and more via zilliz-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lumina2025](https://clawhub.ai/user/lumina2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Zilliz Cloud clusters and Milvus vector database resources from an agent-assisted terminal workflow. It supports cluster lifecycle tasks, collection and vector operations, RBAC, backups, imports, monitoring, billing, and setup guidance for zilliz-cli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-assisted commands can modify or delete live Zilliz Cloud resources, including clusters, databases, collections, backups, and vector data.

Mitigation: Require explicit user confirmation before destructive, RBAC, billing, or data-deletion actions, and prefer reviewed command previews before execution.

Risk: Authentication, user-password, API-key, and payment-card workflows involve sensitive values.

Mitigation: Use browser or interactive terminal flows for secrets and payment cards, and do not paste API keys, passwords, or card details into chat.

Risk: The skill depends on a locally installed zilliz-cli and authenticated cloud context.

Mitigation: Install the CLI in an isolated environment where practical, verify authentication and active context before commands, and use a reviewed or pinned CLI version when available.

## Reference(s):

- [Zilliz Plugin homepage](https://github.com/zilliztech/zilliz-plugin)
- [Zilliz](https://zilliz.com/)
- [Zilliz Cloud](https://cloud.zilliz.com/)
- [ClawHub skill listing](https://clawhub.ai/lumina2025/skills/zilliz-cloud)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-formatted CLI output when commands are run with --output json.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
