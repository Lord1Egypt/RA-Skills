## Description: <br>
Provides structured code review guidance for pull requests, code quality checks, security review, performance analysis, and maintainability assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering reviewers use this skill to inspect pull requests and repository changes, summarize CI status, identify code quality and security issues, and provide actionable review feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may direct an agent to modify repository files, stage changes, commit, or push while handling CI failures. <br>
Mitigation: Require an explicit diff review and user confirmation before applying edits, staging files, committing, or pushing. <br>
Risk: The skill may use GitHub CLI and local repository commands that depend on the user's authenticated account and repository context. <br>
Mitigation: Use it only in trusted repositories or a sandbox, and use least-privilege GitHub credentials when possible. <br>
Risk: Review guidance or proposed fixes can be incomplete or incorrect for the target project. <br>
Mitigation: Treat the output as review assistance, then validate findings with project tests, maintainers, and normal code review before merging. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/terrycode-review) <br>
- [Code Review Reference Guide](artifact/reference.md) <br>
- [Code Review Examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown review comments with optional code snippets and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose repository edits or command execution; review diffs and commands before applying changes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
