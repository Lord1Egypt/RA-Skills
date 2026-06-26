## Description: <br>
Provides structured code review for pull requests and code changes, including code quality, security, performance, maintainability, tests, and CI status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review pull requests or local code changes, check CI failures, and produce prioritized feedback with concrete remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move from review into editing, committing, and pushing repository changes without a clear confirmation step. <br>
Mitigation: Require explicit user approval before applying edits, creating commits, or pushing changes, and review all generated changes before relying on them. <br>
Risk: GitHub CLI commands may use the user's authenticated GitHub session and access pull request or CI information. <br>
Mitigation: Use the skill only in repositories and accounts where the agent is authorized, and confirm the intended PR, branch, and command scope before running GitHub CLI commands. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/terrycarter1985/terry-code-review) <br>
- [Detailed review criteria](artifact/reference.md) <br>
- [Review examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown review findings with code snippets and shell commands when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CI status summaries, prioritized findings, remediation suggestions, and commands for checking pull requests.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
