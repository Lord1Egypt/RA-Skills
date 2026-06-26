## Description: <br>
Comprehensive Rust code review that fans out across detected technology areas, running them in parallel when the agent supports subagents and sequentially otherwise. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for pre-push or pre-PR review of Rust source files. It guides an agent through scope discovery, cargo and clippy checks, technology-specific review, finding verification, and a structured Markdown verdict. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs an agent to inspect Rust source and run local cargo and git commands; Rust build scripts or tests can execute project code. <br>
Mitigation: Review proposed commands before use in sensitive repositories and run checks in a controlled workspace when repository code is untrusted. <br>
Risk: The skill may produce incorrect or misleading review findings if command output is unavailable or source context is incomplete. <br>
Mitigation: Follow the skill's hard gates: list the Rust scope, record unavailable compiler or linter checks, re-read source context for Critical and Major findings, and avoid duplicating compiler or clippy diagnostics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/review-rust) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown review report with file-line findings, command results, and verdict] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local cargo, clippy, check, test, grep, and git commands when available.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
