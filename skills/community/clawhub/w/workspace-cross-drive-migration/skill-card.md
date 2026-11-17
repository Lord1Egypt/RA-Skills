## Description:

把 WorkBuddy 工作空间整体迁移到另一个磁盘，并保留会话历史、项目记忆、项目级技能、自动化绑定与侧边栏显示名。

This skill is ready for commercial/non-commercial use.

## Publisher:

[katyperry13](https://clawhub.ai/user/katyperry13)

### License/Terms of Use:

MIT-0

## Use Case:

面向使用 Windows WorkBuddy/CodeBuddy 的用户，协助他们规划并迁移工作空间，核对会话、记忆和自动化绑定，并在需要时回滚。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Formatting the selected volume can erase its contents.

Mitigation: Prefer an existing compatible destination. Before formatting, confirm the selected volume and keep an independent backup of its contents.

Risk: Manual session-history path edits can cause data loss or leave migration paths inconsistent.

Mitigation: Avoid the manual history-rewrite command until corrected, keep independent backups of the workspace and WorkBuddy data, and review the dry run before applying changes.

Risk: The bundled rollback may not restore every user change.

Mitigation: Keep independent backups and do not treat rollback as a complete backup restore.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/katyperry13/skills/workspace-cross-drive-migration)
- [Storage map](references/storage-map.md)
- [Migration playbook](references/playbook.md)
- [Troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Chinese Markdown guidance and shell command examples, with optional JSON migration plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and migration plans depend on the user's Windows source and destination paths.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
