## Description:

Helps operators inspect and manage Veeam Backup & Replication jobs, repositories, sessions, and VM restores through governed CLI and MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Backup administrators and operations engineers use this skill to check Veeam backup health, investigate failures and repository capacity, manage backup jobs, and initiate or monitor VM restores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write tools can stop backup activity or initiate irreversible restores without an enforced approval or read-only gate.

Mitigation: Begin with a read-only or tightly restricted Veeam account and require independent human approval before restore or session-stop actions.

Risk: A VM restore can overwrite the wrong machine, and its target checks may not identify the backup server under a different display name.

Mitigation: Review the dry-run target and confirm the VM and restore point in the Veeam console before proceeding.

Risk: Leaked master passwords or legacy plaintext credentials could expose Veeam access.

Mitigation: Protect the local credentials directory, avoid committing MCP configurations containing the master password, and migrate legacy plaintext secrets.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zw008/skills/veeam-aiops)
- [Project homepage (skill metadata)](https://github.com/AIops-tools/Veeam-AIops)
- [Agent guardrails](references/agent-guardrails.md)
- [Capabilities](references/capabilities.md)
- [Setup guide](references/setup-guide.md)
- [CLI reference](references/cli-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Text or Markdown with command examples and summarized tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report job, session, repository, or restore status from Veeam tool responses.]

## Skill Version(s):

0.19.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
