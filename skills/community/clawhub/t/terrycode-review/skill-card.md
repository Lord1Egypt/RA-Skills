## Description:

Provides a Japanese code-review workflow for pull requests, code quality checks, security review, performance analysis, and CI/CD status review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review pull requests or local changes, inspect GitHub CI status, and produce prioritized review feedback about quality, security, tests, performance, and maintainability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to fix CI failures and commit or push broad repository changes.

Mitigation: Require explicit user approval before fixes, commits, or pushes; review git status and the staged diff; stage named files instead of using `git add .`.

Risk: The skill may inspect GitHub pull request and CI state through the GitHub CLI.

Mitigation: Use it only in repositories where GitHub CLI access is intended and authenticated; include CI failures as review findings unless the user owns the PR and approves fixes.

Risk: The workflow references `npx bundlephobia`, which can execute a package fetched at runtime.

Mitigation: Avoid the command or pin the package version before running it.

## Reference(s):

- [Code Review skill page](https://clawhub.ai/terrycarter1985/skills/terrycode-review)
- [Detailed review criteria](reference.md)
- [Review examples](examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown review comments with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inspect GitHub pull request and CI status through GitHub CLI when available.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
