## Description:

Backs up, restores, initializes, and syncs a fixed set of core OpenClaw workspace markdown files with the user's private `soul-undead` GitHub repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhao95](https://clawhub.ai/user/zhao95)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to preserve and recover core workspace identity and memory markdown files across reinstalls or machines. It supports syncing local saved changes to a private GitHub repository and restoring that fixed file set back into the OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First initialization can overwrite local OpenClaw identity, memory, and instruction markdown files from remote repository content.

Mitigation: Run it only when that restore behavior is intended, inspect the target private repository first, and rely on the timestamped local snapshot created before restore for rollback.

Risk: Tracked files may be symlinks that lead outside the intended workspace scope.

Mitigation: Inspect the fixed tracked files before execution and avoid running the skill when any tracked workspace file is symlinked.

Risk: The skill copies core workspace files to a private GitHub repository, which can expose sensitive agent identity or memory content to that repository's account and access controls.

Mitigation: Use only a trusted GitHub account and private repository, confirm `gh auth status` is the intended account, and review the files before syncing.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and file path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute a bundled shell script that reads or writes the fixed OpenClaw markdown file set and syncs it with a private GitHub repository.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
