## Description:

Guides agents through uploading local files to GitHub with Git command-line workflows, including repository setup, commits, branch management, Git LFS, and common troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duanc-chao](https://clawhub.ai/user/duanc-chao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare, commit, and push local project files to GitHub while following basic version-control hygiene. It is most useful for routine repository setup, branch workflows, large-file handling, and troubleshooting rejected pushes or messy history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to publish broad local changes to GitHub.

Mitigation: Confirm the repository visibility and review staged files with git status and git diff --cached before pushing.

Risk: Accidentally pushed secrets or private data may remain exposed even after removal from the working tree.

Mitigation: Scan for secrets before pushing; if a secret is pushed, rotate it and clean repository history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duanc-chao/skills/upload)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language procedural guidance for Git and GitHub upload workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
