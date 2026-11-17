## Description:

快速定位 SQL 语句在 PHP/Laravel 代码中的触发位置，通过分析 SQL 结构反向追踪到具体的代码文件、方法和行号

This skill is ready for commercial/non-commercial use.

## Publisher:

[willing-lin](https://clawhub.ai/user/willing-lin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to trace a SQL query back to the PHP/Laravel code path that likely generated it, including files, methods, model relationships, and calling chain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow guides the agent to search and inspect local PHP/Laravel application code.

Mitigation: Use it only in repositories where agent access to application source code is acceptable.

Risk: SQL-to-code tracing can produce multiple possible source locations when query patterns are ambiguous.

Mitigation: Review the reported file paths, methods, line numbers, relationship mappings, and match rationale before acting on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/willing-lin/skills/sql-reflect)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code]

**Output Format:** [Markdown analysis with inline PHP, SQL, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file paths, method names, line numbers, relationship mappings, and multiple candidate source locations when the match is ambiguous.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
