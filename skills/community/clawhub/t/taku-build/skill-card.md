## Description: <br>
Execute an approved implementation plan with visible preflight, update, and completion handoffs, including TDD guidance and optional worktree setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kkenny0](https://clawhub.ai/user/kkenny0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to execute an already-approved implementation plan, choose sequential, parallel, or hybrid execution, preserve a task ledger, and produce verification evidence before review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change project files, run tests, install dependencies, and create worktrees while implementing approved plans. <br>
Mitigation: Review the BUILD PREFLIGHT scope, require confirmation before dependency installs or commits in sensitive repositories, and inspect changed files plus verification evidence before accepting the work. <br>
Risk: Worktree setup may alter repository housekeeping such as adding a project-local worktree path to .gitignore. <br>
Mitigation: Use isolated branches or worktrees for implementation work and review any housekeeping changes separately from feature changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kkenny0/taku-build) <br>
- [Test-Driven Development](references/tdd.md) <br>
- [Git Worktree Isolation](references/worktrees.md) <br>
- [Publisher Profile](https://clawhub.ai/user/kkenny0) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown status blocks with command output summaries and changed-file evidence] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses BUILD PREFLIGHT, BUILD UPDATE, and BUILD COMPLETE handoff formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
