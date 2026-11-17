## Description:

Smart PR Review is an opinionated code-review skill that analyzes PR URLs, local diffs, commits, or files across logic, edge cases, performance, security, maintainability, and architecture, then returns a prioritized review verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fullstackcrew-alpha](https://clawhub.ai/user/fullstackcrew-alpha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review pull requests, local diffs, commits, or individual files before merge. It produces severity-ranked findings, concrete remediation guidance, and an APPROVE, REQUEST CHANGES, or COMMENT verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook mode can send pull request content to Anthropic for automated review.

Mitigation: Install only when that data flow is acceptable, document the review boundary, and avoid sending repositories or pull requests that should not leave the deployment environment.

Risk: The webhook service uses GitHub credentials that can access repository data and post pull request reviews.

Mitigation: Use least-privilege GitHub credentials, protect the token as a secret, rotate it on exposure, and scope access to the repositories that need automated review.

Risk: A public webhook endpoint without strong controls can be abused or triggered by untrusted requests.

Mitigation: Require a non-empty webhook secret, validate GitHub signatures, add body-size and rate limits, and expose the service only through controlled infrastructure.

Risk: Automated review verdicts can be mistaken for human approval.

Mitigation: Do not count bot approvals as human approval and require human maintainers to review blocking findings and merge decisions.

Risk: Unpinned runtime dependencies can change behavior or introduce vulnerabilities after deployment.

Mitigation: Pin dependencies before deployment and review dependency updates through the same code-review process.

## Reference(s):

- [Smart PR Review ClawHub Page](https://clawhub.ai/fullstackcrew-alpha/skills/smart-pr-review)
- [Review Checklist](references/review-checklist.md)
- [Anti-Patterns](references/anti-patterns.md)
- [Review Examples](references/review-examples.md)
- [GitHub CLI](https://cli.github.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown review report with severity sections, code snippets, remediation guidance, and a merge verdict; webhook mode can post the report as a GitHub PR review comment.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese or English output and optional focus on security, performance, logic, or all review dimensions.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
