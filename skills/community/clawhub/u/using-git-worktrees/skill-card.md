## Description: <br>
Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees with smart directory selection and safety verification <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlc000190](https://clawhub.ai/user/zlc000190) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create isolated git worktrees for feature work, run project setup, verify a clean baseline, and report the resulting workspace location. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically change git state by editing .gitignore, creating branches, adding worktrees, and committing ignore changes. <br>
Mitigation: Use it only in repositories where automated worktree setup is intended, and require confirmation before edits or commits in untrusted or sensitive repositories. <br>
Risk: The skill may run dependency installation, build, and test commands as part of setup. <br>
Mitigation: Review the repository and command plan before allowing install, build, or test commands, especially when working with untrusted code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlc000190/using-git-worktrees) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose git worktree creation, .gitignore edits, dependency installation, builds, tests, and baseline status reporting.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
