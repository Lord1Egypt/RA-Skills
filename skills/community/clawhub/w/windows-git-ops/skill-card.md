## Description:

Use this skill when performing Git operations in a Windows PowerShell workspace, especially for branch creation, staging, commit, merge, status inspection, and command construction that must avoid bash-only syntax and reduce shell mistakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangchaoqing5](https://clawhub.ai/user/zhangchaoqing5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to perform auditable Git operations in Windows PowerShell workspaces. It helps agents inspect repository state, create branches, stage intended files, commit changes, and merge without relying on bash-only shell syntax.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide repository mutations such as staging, committing, branching, and merging.

Mitigation: Review the intended Git changes before approving commands, and inspect branch, status, unstaged files, and staged files before mutating repository state.

Risk: Broad staging or destructive Git commands could include or discard unrelated user changes.

Mitigation: Stage only explicit intended paths and do not revert, reset, or discard user changes unless the user explicitly requests it.

Risk: Bash-only command patterns can fail or behave unexpectedly in Windows PowerShell.

Mitigation: Use one PowerShell-safe command per invocation and rewrite environment variables, quoting, sequencing, and redirection in native PowerShell form.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangchaoqing5/skills/windows-git-ops)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown guidance with inline PowerShell and Git command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emphasizes non-interactive commands, targeted repository inspection, explicit staging, and concise reporting of Git results.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
