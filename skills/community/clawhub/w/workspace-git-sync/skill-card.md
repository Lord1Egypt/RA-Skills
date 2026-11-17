## Description:

Syncs an OpenClaw workspace directory to a specified local Git repository and can run git add, commit, and push operations for backup and version control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[david668haha](https://clawhub.ai/user/david668haha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to back up or archive an OpenClaw workspace into a dedicated Git repository. It is intended for mirror-style workspace backup workflows that require automated pull, copy, commit, and push steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete files from the chosen target Git repository while mirroring workspace contents.

Mitigation: Use a dedicated backup repository and avoid targeting an existing project repository with unrelated or uncommitted files.

Risk: The skill can push broad workspace contents to a remote repository, which may expose secrets or private data.

Mitigation: Review the workspace for secrets and confirm the repository origin and visibility before syncing.

Risk: The force sync path can affect remote history.

Mitigation: Avoid force_sync unless the user understands the remote-history impact and has verified the target branch.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/david668haha/skills/workspace-git-sync)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to run local Git sync commands against a user-specified repository.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
