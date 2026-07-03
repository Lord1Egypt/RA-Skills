## Description: <br>
Review Workflow coordinates change-background collection, structured code review, debugging and fix guidance, commit-message generation, and Git operation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeautifulsnow](https://clawhub.ai/user/abeautifulsnow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review local code changes, reason about fixes, prepare conventional commit messages, and receive Git command guidance before submitting work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect repository diffs and untracked non-ignored file contents into review artifacts. <br>
Mitigation: Before running it, ensure secrets, private keys, .env files, drafts, and other sensitive local files are ignored or removed from the working tree. <br>
Risk: The skill may suggest git add, commit, push, or force-with-lease commands as part of the workflow. <br>
Mitigation: Review and confirm each suggested Git command before execution, and avoid staging files that contain sensitive or unrelated changes. <br>
Risk: Broad activation triggers can start the review workflow in repositories where the user did not intend to collect change context. <br>
Mitigation: Use the skill only in the intended repository and inspect generated review artifacts before sharing or reusing them. <br>


## Reference(s): <br>
- [Code Reviewer](references/code-reviewer/SKILL.md) <br>
- [Common Bugs Checklist](references/code-reviewer/references/common-bugs-checklist.md) <br>
- [Security Review Guide](references/code-reviewer/references/security-review-guide.md) <br>
- [Parallel Debugging](references/parallel-debugging/SKILL.md) <br>
- [Hypothesis Testing](references/parallel-debugging/references/hypothesis-testing.md) <br>
- [Git Commit](references/git-commit/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with structured reports, diffs, commit messages, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create structured review artifacts such as review_diff.json and review_classified.json when its helper scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
