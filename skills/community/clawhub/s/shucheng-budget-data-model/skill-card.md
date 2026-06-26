## Description: <br>
提供预算系统数据模型的完整定义，包括所有表名、字段名、数据类型等。当用户需要查询预算相关数据模型结构、编写数据查询脚本、或需要了解特定表的字段信息时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lan2898408767](https://clawhub.ai/user/lan2898408767) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and budget-system maintainers use this skill to identify budget database tables, fields, data types, and query patterns for budget and finance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL or DataModelUtils snippets may be incorrect or unsafe for live budget or financial systems. <br>
Mitigation: Verify table names, field names, query conditions, and permissions before running generated queries; test against non-production data first. <br>
Risk: The schema reference may become stale if the underlying budget system changes. <br>
Mitigation: Compare recommendations against the current approved data model before using them for production reports or automation. <br>


## Reference(s): <br>
- [Data model reference](references/data_models.json) <br>
- [ClawHub skill page](https://clawhub.ai/lan2898408767/shucheng-budget-data-model) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with schema summaries and Groovy/DataModelUtils query examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reference guidance only; no executable binaries or external tools are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
