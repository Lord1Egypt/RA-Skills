## Description:

SQL Master helps agents generate, diagnose, optimize, and explain SQL across major database dialects, with optional data loading, export, visualization, and report-pipeline workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moniq888](https://clawhub.ai/user/moniq888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and data analysts use this skill to draft and review SQL, inspect execution plans, design indexes and schemas, load database or file data, convert query results, and coordinate downstream visualization or reporting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pickle file loading can execute code during deserialization.

Mitigation: Do not load untrusted .pkl or .pickle files; prefer trusted CSV, JSON, Parquet, Excel, or database sources.

Risk: Database execution and export workflows can access or modify sensitive data when broad credentials are used.

Mitigation: Use read-only or least-privilege database accounts, review SQL before execution, and verify output paths before writing exports.

Risk: Companion skill integration expands the trust boundary for visualization and report generation.

Mitigation: Use only trusted sql-dataviz and sql-report-generator installations, and review generated charts, reports, and insights before sharing.

Risk: Range-based Python dependencies may resolve differently across environments.

Mitigation: Pin and review dependencies before production or sensitive-environment deployment.

## Reference(s):

- [CLI 实操速查](references/cli-quickref.md)
- [数仓建模 & 分层架构](references/data-warehouse.md)
- [DDL 设计规范](references/ddl-design.md)
- [多方言差异速查](references/dialect-guide.md)
- [Hive 数据倾斜：大厂生产级深化补充](references/hive-skew-advanced.md)
- [索引设计策略](references/index-design.md)
- [慢查询诊断 & 执行计划分析](references/query-optimization.md)
- [SQL 生成指南](references/sql-generation.md)
- [SQL 原理深度](references/sql-internals.md)
- [SQL 安全规范](references/sql-security.md)
- [SQL 查询结果可视化指南](references/visualization-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown prose with SQL, Python, and shell snippets, plus optional CSV, JSON, Excel, Parquet, SQLite, PNG, HTML, or report file outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local database and file connector scripts, and may hand off to trusted sql-dataviz or sql-report-generator companion skills when available.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
