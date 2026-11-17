## Description:

生产现场隐患排查与整改跟踪；用于日常安全检查、隐患录入、统计分析、整改任务管理及合规性评估；帮助企业建立隐患闭环管理机制

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Production safety staff and operations teams use this skill to record workplace hazards, track remediation tasks, and generate inspection summaries from local JSON records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inspection and remediation data is stored locally under ./inspection_data/, so records may be lost if the directory is deleted or not backed up.

Mitigation: Keep regular backups of ./inspection_data/ before and after inspection or remediation updates.

Risk: Concurrent script runs may overwrite local JSON inspection or remediation records.

Mitigation: Run one update command at a time or place the data directory under an external locking or review process.

Risk: The checklist and scripts support record keeping but do not provide a complete compliance assessment.

Mitigation: Require qualified human review for compliance decisions, high-severity hazards, and final remediation closure.

## Reference(s):

- [生产现场隐患排查清单](references/inspection_checklist.md)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-hazard-inspection)
- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-hazard-inspection)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local JSON files under ./inspection_data/ when its scripts are run.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
