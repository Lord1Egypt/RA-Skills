## Description:

团队周报助手 — 自动收集团队工作进展，生成结构化周报/月报

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanjing5024064](https://clawhub.ai/user/hanjing5024064)

### License/Terms of Use:

MIT-0

## Use Case:

Team leads and project managers use this Chinese-language agent to maintain team rosters, record worklogs, and generate structured weekly or monthly status reports with workload analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Team rosters and individual worklogs may contain personal or confidential project information stored on disk.

Mitigation: Use a private TW_DATA_DIR with appropriate filesystem access controls, and avoid entering highly sensitive HR or confidential project details unless suitable controls exist.

Risk: Member management actions can remove local team records.

Mitigation: Review delete requests and the current team data before running destructive commands.

Risk: Generated Markdown and Mermaid reports may include user-provided text.

Mitigation: Render generated reports in a hardened Markdown/Mermaid viewer when records may include untrusted input.

## Reference(s):

- [周报模板参考](references/weekly-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese-language text with shell commands, JSON CLI responses, and Markdown reports that may include Mermaid diagrams]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores team and worklog records in local JSON files under TW_DATA_DIR; paid features add monthly reports, charts, trends, and Gantt output.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
