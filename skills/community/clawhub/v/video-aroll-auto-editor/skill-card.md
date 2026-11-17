## Description:

Automates rough editing for single-person talking-head videos by detecting silence, scoring speech segments, removing duplicate takes, and producing selected clips with reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gilbertwuu](https://clawhub.ai/user/gilbertwuu)

### License/Terms of Use:

MIT-0

## Use Case:

Video creators and production teams use this skill to automate first-pass rough cuts for A'Roll footage, especially Chinese monologue-style vlogs, tutorials, podcasts, and knowledge-sharing videos. It supports single-video clipping and batch deduplication with concatenated output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch cleanup can recursively delete a user-supplied work directory without sufficient guardrails.

Mitigation: Run only in a fresh dedicated temporary work directory, avoid privileged execution, and review batch-mode paths before starting processing.

Risk: Video filenames and input directories from untrusted sources may interact with shell-adjacent media tooling and cleanup behavior.

Mitigation: Use trusted local media files, keep inputs separate from important directories, and inspect output and work directory arguments before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gilbertwuu/skills/video-aroll-auto-editor)
- [README](artifact/README.md)
- [Technical Documentation](artifact/CODE_DOCUMENTATION.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples; generated runtime artifacts include MP4 clips and Markdown reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.8+, FFmpeg/ffprobe, and openai-whisper for transcription-aware scoring; supports .MTS, .mp4, and .mov inputs.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
