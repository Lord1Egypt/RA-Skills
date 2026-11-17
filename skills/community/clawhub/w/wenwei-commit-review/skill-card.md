## Description:

Reviews Git diffs before commit to identify newly introduced bugs, security risks, regression risks, and optimization opportunities in a structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wed840313](https://clawhub.ai/user/wed840313)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before committing code to review staged, unstaged, or untracked changes and decide whether fixes are needed before commit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect git diffs, untracked files, and nearby repository context, which can include secrets or private data.

Mitigation: Run it only on repositories and changes suitable for the agent conversation; remove or mask sensitive values before review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wed840313/skills/wenwei-commit-review)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown review report with categorized findings and commit readiness guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports focus on changed code and include file paths, line references, severity categories, remediation suggestions, and a submit-or-fix conclusion.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
