## Description:

Reviews a GitHub pull request end to end - fetches the diff, runs checks, analyzes with three parallel agents (correctness, conventions, efficiency), validates every finding against the code, drafts inline comments with a recommended action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenequm](https://clawhub.ai/user/tenequm)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to review GitHub pull requests by collecting PR context, running agreed checks, analyzing changed code for correctness, convention, efficiency, and safety issues, and preparing review comments for explicit user approval before posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access target repository contents and active GitHub CLI credentials.

Mitigation: Use it only in repositories where agent access and the authenticated GitHub account are appropriate, and verify the target repository and review action before posting.

Risk: A predictable temporary review payload path could allow local tampering before an authenticated GitHub review is submitted.

Mitigation: Replace the fixed /tmp/pr-review.json workflow with mktemp or stdin piping and remove temporary payloads after submission.

Risk: Pull request descriptions, diffs, commit messages, and changed files are untrusted inputs that may try to influence agent behavior.

Mitigation: Keep PR-sourced content delimited as untrusted data and do not execute commands sourced from PR content or changed files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tenequm/skills/review-github-pr)
- [Skill homepage](https://github.com/tenequm/skills/tree/main/skills/review-github-pr)
- [Publisher profile](https://clawhub.ai/user/tenequm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown review draft with inline code suggestions and optional JSON payload guidance for GitHub review posting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces findings grouped by severity, a recommended review action, and a confirmation prompt before posting.]

## Skill Version(s):

0.5.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
