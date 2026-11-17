## Description:

A local visual LRC lyric editor for creating, importing, timing, previewing, and exporting synchronized lyric files from audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiyunnet](https://clawhub.ai/user/xiyunnet)

### License/Terms of Use:

MIT-0

## Use Case:

External users and lyric creators use this skill to launch a local browser-based editor for making new LRC lyric files, correcting existing lyric timing, and exporting synchronized lyrics for media players.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local network service is unauthenticated and may be reachable beyond the user's machine.

Mitigation: Run only in a trusted local environment and prefer binding the service to localhost before broader use.

Risk: The upload path handling and shutdown route were flagged by security evidence as requiring review.

Mitigation: Review and harden upload handling and service shutdown behavior before using shared or privileged accounts.

Risk: Dependency pinning and resource limits were flagged as unresolved security concerns.

Mitigation: Pin dependencies and set appropriate upload and processing limits before deploying beyond personal local use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiyunnet/skills/xi-lrc-editor)
- [FFmpeg downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and local browser workflow details; the launched app exports LRC text files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local web app accepts audio and LRC inputs, stores edits in browser local storage, and exports standard .lrc files.]

## Skill Version(s):

1.1.0 (source: release evidence and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
