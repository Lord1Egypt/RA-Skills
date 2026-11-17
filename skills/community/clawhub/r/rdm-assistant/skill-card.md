## Description:

研发经理助手帮助研发经理生成晨会和周报、汇总代码活动、创建代码审查清单，并基于项目配置跟踪进度和任务分配建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangminjun](https://clawhub.ai/user/wangminjun)

### License/Terms of Use:

MIT

## Use Case:

External development managers and engineering leads use this skill to prepare recurring project reports, inspect Git activity, structure code reviews, monitor project progress, and draft task allocation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Git statistics tool can unexpectedly change a repository's active branch.

Mitigation: Review and update the Git statistics workflow before use so it inspects the requested branch without changing the user's working branch.

Risk: Report and checklist tools may overwrite existing local output files.

Mitigation: Require explicit confirmation or unique output paths before writing generated reports or review checklists.

Risk: The skill reads configured local repositories and project configuration.

Mitigation: Install and run it only in workspaces where the operator is comfortable exposing repository metadata to the agent workflow.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wangminjun/skills/rdm-assistant)
- [README](README.md)
- [Code review checklist](docs/代码审查检查清单.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, checklist files, shell command output, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read configured local Git repositories and write Markdown reports or review checklists to local output paths.]

## Skill Version(s):

1.0.3 (source: frontmatter and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
