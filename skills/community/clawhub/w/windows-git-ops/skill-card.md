## Description: <br>
Use this skill when performing Git operations in a Windows PowerShell workspace, especially for branch creation, staging, commit, merge, status inspection, and command construction that must avoid bash-only syntax and reduce shell mistakes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangchaoqing5](https://clawhub.ai/user/zhangchaoqing5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and perform Git operations in Windows PowerShell while keeping branch, staging, commit, and merge actions explicit and auditable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository-changing Git commands could affect unintended files or branches. <br>
Mitigation: Inspect the current branch, worktree status, unstaged changes, and staged files before branch, commit, or merge operations. <br>
Risk: A command copied from a bash-oriented workflow can fail or behave unexpectedly in Windows PowerShell. <br>
Mitigation: Use separate PowerShell-safe Git invocations and rewrite shell-specific syntax before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Markdown with inline PowerShell and Git command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [PowerShell-safe, non-interactive Git command sequences.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
