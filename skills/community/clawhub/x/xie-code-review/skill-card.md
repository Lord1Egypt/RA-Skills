## Description:

Automated code review assistant. Analyzes code changes, PRs, and files for quality issues, best practices, security concerns, and style violations. Provides actionable feedback with line-by-line comments and summary reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review files, staged changes, commits, or diff files for code quality, style, best-practice, and security issues. It can produce line-level findings and summary reports for local workflows, pre-commit checks, or CI review artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can load optional Python modules from a c-support/lib path outside the skill package.

Mitigation: Install and run it only in a trusted skills directory, or remove or sandbox the optional C-support import path before use.

Risk: The skill reads target files and runs git queries for staged or commit reviews.

Mitigation: Run it only against intended repositories and files in a controlled workspace with appropriate access boundaries.

Risk: The skill can write Markdown or JSON reports to a user-supplied output path.

Mitigation: Use explicit output paths in controlled locations and review generated reports before using them in CI or release decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michealxie001/skills/xie-code-review)
- [Publisher profile](https://clawhub.ai/user/michealxie001)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown report by default, with optional JSON report output and optional saved report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include issue counts, file-level findings, severity labels, metrics, and suggested fixes when available.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
