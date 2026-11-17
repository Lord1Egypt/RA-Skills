## Description:

帮助代理下载 GitHub 仓库或 npm 包源码，分析 AI Agent 架构、工具定义和提示词工程，并生成结构化 Markdown 报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgugeng](https://clawhub.ai/user/lgugeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect agent repositories, packages, and binaries they are authorized to analyze, with emphasis on architecture, tool definitions, permission models, prompt fragments, configuration, and reusable design patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extraction reports can contain sensitive source, prompt, configuration, or environment-variable fragments and may be written to predictable temporary paths.

Mitigation: Choose a private output directory with restrictive permissions, review report contents before sharing, and delete reports when analysis is finished.

Risk: The workflow can be applied to repositories, packages, or binaries that the user is not authorized to analyze.

Mitigation: Use the skill only on targets you are permitted to inspect and respect applicable project, package, and platform terms.

## Reference(s):

- [AI Agent 分析参考手册](references/ai-agent-patterns.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown report with command snippets and structured analysis sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include extracted source, prompt, tool, configuration, and environment-variable fragments from the analyzed target.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
