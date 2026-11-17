## Description:

Coordinates adversarial code review, independent verification, and neutral adjudication to identify defects and guide tested fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[revolutionla](https://clawhub.ai/user/revolutionla)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review code changes before merging or release, cross-check findings, and plan fixes with regression tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers can lead to repository-wide inspection and local command execution.

Mitigation: Specify a narrow review scope and approve commands before they run.

Risk: The workflow can edit code and tests without an explicit confirmation checkpoint.

Mitigation: Require approval before remediation and review proposed changes and test results.

Risk: Review reports may contain sensitive repository details.

Mitigation: Keep private-project reports out of published repositories and verify their visibility before sharing.

Risk: Bundled installers can fetch changing content from a publisher-controlled GitHub branch.

Mitigation: Avoid the install scripts unless you trust that source; inspect and pin the content before installation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/revolutionla/skills/three-party-adversarial-review)
- [Quickstart](references/quickstart.md)
- [Review dimensions](references/review-dimensions.md)
- [Role prompt templates](references/prompt-templates.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands]

**Output Format:** [Markdown review reports and remediation summaries, with optional code changes and tests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports distinguish verified findings, deferred fixes, and unverified claims.]

## Skill Version(s):

2.5.1 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
