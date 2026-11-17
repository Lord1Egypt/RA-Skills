## Description:

Python Arch Optimizer helps agents analyze and refactor Python project structure toward common engineering best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jjflydudu](https://clawhub.ai/user/jjflydudu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess Python project layout, dependency management, code organization, testing structure, and CI/CD configuration, then plan or run guarded restructuring steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted project name or output path could cause generated files to be written outside the intended folder.

Mitigation: Use only trusted project names and output paths, review dry-run or planned changes first, avoid --force unless the destination has been checked, and add path-containment validation before use on important workspaces.

Risk: Migration commands can move or create files in an existing Python project.

Mitigation: Require explicit user confirmation, prefer --dry-run before execution, inspect the generated plan, and rely on backups and rollback if execution fails.

## Reference(s):

- [Python Project Architecture Best Practices](artifact/references/best-practices.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON or text analysis, inline shell commands, and generated configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project structure reports, refactoring plans, dry-run migration commands, and generated file content.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
