## Description:

Review Workflow orchestrates change-context collection, structured code review, debugging and fix suggestions, test and regression checks, commit message generation, and Git workflow guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeautifulsnow](https://clawhub.ai/user/abeautifulsnow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review local code changes with explicit change context, language-aware review rules, fix proposals, test validation, and commit preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may collect tracked diffs and untracked file contents, which can expose local secrets or private work-in-progress.

Mitigation: Run it only in repositories prepared for review, remove untracked secrets first, and require explicit approval before collecting untracked files.

Risk: The workflow may run broad lint, format, test, dependency-scan, and npx-based commands that can modify files or execute project tooling.

Mitigation: Review planned commands before execution, prefer explicit approval for auto-fix steps, and inspect resulting diffs before committing.

Risk: The workflow can provide Git push, rebase, and history-management guidance that may affect shared branches if followed carelessly.

Mitigation: Treat Git commands as guidance, verify the target branch and remote, and require human confirmation before push or history-rewriting operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeautifulsnow/skills/review-workflow)
- [Server-resolved GitHub provenance](https://github.com/Abeautifulsnow/skills/tree/main/review-workflow)
- [Review preferences](references/review-preferences/SKILL.md)
- [Code reviewer](references/code-reviewer/SKILL.md)
- [Parallel debugging](references/parallel-debugging/SKILL.md)
- [Git commit](references/git-commit/SKILL.md)
- [Code review best practices](references/code-reviewer/references/code-review-best-practices.md)
- [Security review guide](references/code-reviewer/references/security-review-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports with inline diffs, shell commands, and commit message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce structured review reports, patch suggestions, test summaries, secret-scan results, and Git command guidance.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; source skill frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
