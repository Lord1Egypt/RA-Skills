## Description:

Manage explicitly requested vwsd multi-repository workspaces: inspect status, configure local and remote sources, prepare Git worktrees, sync, preview pushes, diagnose problems, and plan cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albert-lv](https://clawhub.ai/user/albert-lv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to configure, inspect, sync, publish authorized changes from, diagnose, and safely clean up vwsd workspaces spanning local or remote repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing workspace commits can send selected changes to remote repositories.

Mitigation: Preview with vwsd push --name <workspace> --json, confirm the repositories, branches, and commits, and publish with --yes only when authorized.

Risk: Unmounting or destroying a workspace can delete worktree files, configuration, caches, and local-only commits.

Mitigation: Resolve the affected paths and inspect tracked, untracked, ignored, branch, upstream, and unpushed-commit state; preserve data or obtain explicit authorization for identified loss before cleanup.

Risk: Installing or building vwsd may execute code that has not been sufficiently verified.

Mitigation: Install only when requested; verify a release signature or provenance and digest, or review a pinned source revision, build scripts, and dependencies before building.

## Reference(s):

- [Installation guidance](references/installation.md)
- [Project homepage (Clawdis metadata)](https://github.com/nano-harness/virtual-workspace)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell command examples and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command sequences, workspace configuration examples, and operational safeguards.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
