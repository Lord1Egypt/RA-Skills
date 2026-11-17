## Description:

Helps coding agents review local changes, create and review GitHub pull requests or GitLab merge requests, and list a user's open requests or commits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yexinjia](https://clawhub.ai/user/yexinjia)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to review repository changes, create or review PRs/MRs, and inspect their open requests or authored commits through a Git automation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default review configuration can automatically approve and merge PRs/MRs.

Mitigation: Set pullRequestReview.autoApprove=false and pullRequestReview.autoMerge=false before live or batch review, or request a dry run.

Risk: Git automation can stage, commit, push, and create PRs/MRs in a repository.

Mitigation: Review the selected mode and configuration before execution, and use the least-privileged platform token suitable for the task.

Risk: If no compatible CLI is found, the skill can install its CLI globally without asking.

Mitigation: Confirm that a global CLI installation is acceptable before enabling the skill.

## Reference(s):

- [smart-git release](https://clawhub.ai/yexinjia/skills/smart-git)
- [smart-commit-host-agent package](https://www.npmjs.com/package/smart-commit-host-agent)
- [Setup guide](SETUP.md)
- [Configuration guide](CONFIG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown summaries with review findings and command or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depending on the selected mode, the workflow can create commits, push changes, or publish PR/MR reviews.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
