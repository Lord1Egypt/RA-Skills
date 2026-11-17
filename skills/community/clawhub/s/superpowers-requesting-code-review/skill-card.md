## Description:

Request code reviews with precise context after tasks, major features, or before merges to catch issues early and ensure code meets requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[demo112](https://clawhub.ai/user/demo112)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to request structured code reviews for completed tasks, feature work, bug fixes, refactors, and pre-merge changes. It guides reviewers to compare code changes against requirements, assess readiness, and categorize issues by severity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review guidance can miss issues or produce incorrect feedback if the reviewer is given incomplete requirements or the wrong git range.

Mitigation: Provide the intended requirements, base SHA, head SHA, and a concise implementation summary before acting on the review.

Risk: The workflow inspects git diffs and may expose repository code to a reviewer subagent.

Mitigation: Use it only in repositories where code review by the configured agent or subagent is permitted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/demo112/skills/superpowers-requesting-code-review)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and review templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces code review request guidance and a structured review report format; no hidden install, persistence, credential, network, or destructive behavior was found in security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
