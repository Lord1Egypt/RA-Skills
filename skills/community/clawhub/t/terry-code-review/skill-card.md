## Description:

Provides structured code review support for pull requests and code changes, including CI status checks, code quality review, security inspection, performance analysis, and maintainability feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review pull requests and local code changes, check CI status, identify security and quality issues, and produce prioritized review feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask an agent to modify, broadly stage, commit, and push repository code while resolving CI failures.

Mitigation: Inspect the exact diff, exclude secrets and unrelated files, and require explicit approval before staging, committing, or pushing changes.

Risk: The skill depends on GitHub CLI access and may read CI logs or PR metadata.

Mitigation: Use it only in repositories where that access is acceptable and keep GitHub authentication scoped to the work being reviewed.

Risk: The skill references a global agent configuration file as review policy.

Mitigation: Use that policy only when the global configuration is trusted, or provide explicit project-local review criteria.

## Reference(s):

- [Code Review Reference Guide](artifact/reference.md)
- [Code Review Examples](artifact/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/terry-code-review)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prioritized findings, CI status summaries, concrete remediation suggestions, and optional commands for local verification.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
