## Description:

Automates OpenClaw workspace health checks and optional repairs for redundant files, memory-file naming, script permissions, and Git changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyi881](https://clawhub.ai/user/zhangyi881)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace maintainers use this skill to inspect OpenClaw workspaces, produce health reports, and optionally apply maintenance fixes across files, script permissions, and Git state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The --fix mode may move root-level files into tmp/, rename memory files, change PowerShell script permissions, and automatically commit current Git changes.

Mitigation: Run in a disposable or clean repository, inspect git status first, and avoid --fix unless dry-run, confirmation, and narrow file selection controls are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangyi881/skills/workspace-auto-maintenance)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text terminal report with documented shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify workspace files, permissions, and Git state when run with --fix.]

## Skill Version(s):

1.0.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
