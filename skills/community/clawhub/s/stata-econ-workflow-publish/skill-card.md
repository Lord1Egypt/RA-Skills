## Description:

Manages Stata-based empirical economics workflows, including do-file authoring, execution guidance, project structure, replication checks, econometric review, log verification, and quality gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xht-322](https://clawhub.ai/user/xht-322)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, economics analysts, and developers use this skill to structure Stata empirical research projects, write and run do-files, verify logged results, review econometric choices, and prepare reproducible analysis outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent agent-memory behavior may record project context in MEMORY.md, TOOLS.md, or CLAUDE.md.

Mitigation: Review, remove, or constrain the memory-learning behavior before installing the skill in a research repository.

Risk: Git-hook behavior may persist after installation and run automatically during commits.

Mitigation: Inspect the pre-commit hook before installing it, and install it only when the repository owner accepts the persistent behavior.

Risk: External tooling commands such as uvx, npm, and pip may install or run unpinned dependencies.

Mitigation: Pin external tool versions and review commands before execution.

Risk: Stata workflows can handle sensitive raw or derived research data.

Mitigation: Use the skill only in trusted Stata research repositories and follow the included data-protection protocol before committing files.

## Reference(s):

- [codex-stata-for-economists](https://github.com/maxwell2732/codex-stata-for-economists)
- [Stata-MCP](https://github.com/sepinetam/stata-mcp)
- [Stata-MCP documentation](https://docs.statamcp.com)
- [Attribution](ATTRIBUTION.md)
- [Workflow quick reference](references/workflow-quickref.md)
- [Replication-first protocol](references/replication-first.md)
- [Log verification protocol](references/log-verification.md)
- [Quality gates](references/quality-gates.md)
- [Data protection protocol](references/data-protection.md)
- [Stata coding convention](references/stata-coding-convention.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Stata, shell, and PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce review reports, quality scores, project templates, Stata do-file guidance, and replication workflow recommendations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
