## Description:

电脑文件管理技能。当用户要求清理垃圾文件、整理文档、检测重复文件、备份文件夹，或提到文件管理、磁盘清理、文件整理、重复文件、文件备份等相关操作时使用此技能。原生支持 macOS、Linux 和 Windows。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yy756127197](https://clawhub.ai/user/yy756127197)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to inspect local folders, identify cleanup candidates or duplicate files, organize files, create backups, and roll back logged file moves or trash operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move, trash, copy, and restore files within the current user's permissions.

Mitigation: Use it only on explicitly chosen folders and review every planned change before allowing write operations.

Risk: Broad targets such as Home, system directories, app configuration folders, and cache roots may expose more files than intended.

Mitigation: Prefer narrow project or download subfolders and avoid broad roots unless the file list has been carefully reviewed.

Risk: Rollback can act on operation logs and may restore or move files based on log contents.

Mitigation: Run rollback only against log files you created or inspected, and verify the target paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yy756127197/skills/super-file-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured file-operation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSONL operation logs when move, trash, or rollback workflows are used.]

## Skill Version(s):

2.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
