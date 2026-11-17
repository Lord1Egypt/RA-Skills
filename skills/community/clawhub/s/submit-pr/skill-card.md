## Description:

Standardizes pull request submission by guiding secret scanning, file scope confirmation, commit message creation, pushing, and GitHub PR creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mykelio1001](https://clawhub.ai/user/mykelio1001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when preparing a pull request from local repository changes. It guides them through scanning for sensitive information, confirming the files to include, creating a conventional commit, pushing the branch, and opening a GitHub pull request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can stage, commit, push, and create GitHub pull requests.

Mitigation: Use it only in repositories where the user is comfortable allowing those Git and GitHub actions, and review the branch and file list before confirming.

Risk: The PR title may be unsafe if it contains shell metacharacters, quotes, command substitutions, or newlines.

Mitigation: Use simple PR titles until the skill validates title input before passing it to shell commands.

Risk: Secret scanning may be incomplete before code is pushed.

Mitigation: Manually review untracked files, staged changes, and secrets before confirming the push and PR creation steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mykelio1001/skills/submit-pr)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown status report with shell commands, commit text, and pull request content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before staging files and committing changes.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
