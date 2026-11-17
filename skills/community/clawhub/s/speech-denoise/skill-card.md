## Description:

Speech enhancement and vocal denoising on a remote L4 GPU for local audio or video files, returning noise-reduced speech audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[speech2srt](https://clawhub.ai/user/speech2srt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to clean noisy speech recordings or audio/video files by uploading selected media to Modal, running GPU speech enhancement, and retrieving enhanced WAV files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media files are uploaded to Modal for remote processing.

Mitigation: Use only recordings that are appropriate to upload to Modal and avoid sensitive or confidential audio or video.

Risk: Unsafe task-name path handling can affect unintended remote files or directories.

Mitigation: Use a simple generated slug rather than a custom path-like value.

Risk: The skill creates Modal volumes and runs remote GPU code with mutable dependencies.

Mitigation: Review the skill before installing and monitor Modal resources created during use.

## Reference(s):

- [Error Handling](references/error-handling.md)
- [ClawHub Skill Page](https://clawhub.ai/speech2srt/skills/speech-denoise)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and generated WAV audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces enhanced WAV files with an _enhanced suffix and reports processed file count, result paths, sizes, and real-time factor.]

## Skill Version(s):

v1.3.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
