## Description:

Reviews code changes from a testing perspective to identify affected areas, high-risk patterns, and a focused regression test scope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and testers use this skill to review pull requests or diffs for change impact, test gaps, and targeted regression scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional installation command fetches an unpinned package.

Mitigation: Only install from a trusted source, or pin and verify the package first.

Risk: The review reads repository diffs and related code, which may contain sensitive information.

Mitigation: Limit access to the intended repository and avoid sharing sensitive code in review outputs.

## Reference(s):

- [Testing-focused code review lens](references/cr-lens.md)
- [ClawHub skill release](https://clawhub.ai/kokxi/skills/qa-code-review-for-test)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes review findings, test gaps, impact analysis, risk patterns, and a regression scope with a review ID.]

## Skill Version(s):

1.8.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
