## Description:

Stages changes, creates a conventional commit, pushes a branch, and opens a draft GitHub pull request using the GitHub CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patrick-erichsen-2](https://clawhub.ai/user/patrick-erichsen-2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to package completed repository work for review by staging intended changes, committing them, pushing a branch, and opening a draft pull request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad staging and pushing can include secrets, unrelated files, or unintended changes in a commit and remote branch.

Mitigation: Review the full working tree, inspect status and diffs, and remove secrets or unrelated files before invoking the skill.

Risk: Dependency or tool installation during checks can execute commands in an untrusted repository context.

Mitigation: Do not allow installation unless the repository is trusted and the exact install command has been reviewed and approved.

Risk: Automated push and pull request creation can publish work to the wrong remote branch.

Mitigation: Confirm the active branch, upstream remote, and target branch are safe before pushing or opening the pull request.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create commits, push branches, and draft pull request descriptions through the local Git and GitHub CLI environment.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
