## Description: <br>
团队周报助手 — 自动收集团队工作进展，生成结构化周报/月报 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanjing5024064](https://clawhub.ai/user/hanjing5024064) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Team leads and project managers use this skill to maintain team member records, capture work logs, and generate Chinese weekly or monthly status reports with summaries, tables, Mermaid charts, and workload insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Team names, roles, projects, work descriptions, hours, and performance-related summaries are stored as local JSON files. <br>
Mitigation: Set TW_DATA_DIR to a protected location and limit access to the stored team and work-log files. <br>
Risk: Generated reports may contain sensitive operational or performance information that could be shared too broadly. <br>
Mitigation: Review weekly, monthly, and analysis reports before sharing them outside the intended audience. <br>
Risk: Member removal and work-log changes alter local records. <br>
Mitigation: Confirm add, remove, and delete-style actions carefully before running the associated commands. <br>


## Reference(s): <br>
- [周报模板参考](references/weekly-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese conversational guidance plus JSON tool results and Markdown reports with tables and Mermaid diagrams] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TW_SUBSCRIPTION_TIER for feature limits and TW_DATA_DIR for local JSON data storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
