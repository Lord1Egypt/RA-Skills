## Description:

Safely send local files, images, audio, video, and other media through QQBot by staging a disposable copy, sending it with <qqmedia>, and cleaning up only the staged file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjuncher](https://clawhub.ai/user/zjuncher)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to send user-requested local files or URL media through QQBot while preserving the original local file. It is intended for workflows that need a complete stage, send, and temporary cleanup flow rather than returning a local path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cleanup helper can delete files inside ~/.openclaw/media/qqbot/ when invoked with --cleanup.

Mitigation: Use cleanup only with the exact staged path printed during the same send operation, and never with original source paths, guessed paths, URLs, or earlier staged files.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and <qqmedia> media references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stages local files up to 100 MB into the QQBot media relay directory and cleans up only the staged copy.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
