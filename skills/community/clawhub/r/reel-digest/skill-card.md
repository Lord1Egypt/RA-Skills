## Description:

Reel Digest downloads a video or reel from a URL, extracts frames, transcribes audio, and helps an agent produce a structured content, visual, and marketing analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casperzinou](https://clawhub.ai/user/casperzinou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, marketers, and analysts use this skill to turn a video URL into a concise digest of transcript content, key frames, visual strategy, engagement tactics, and business signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied video URLs and output paths may be handled unsafely by the included scripts.

Mitigation: Run only in a restricted environment, avoid untrusted video links, and do not use attacker-controlled output directories.

Risk: The downloader/transcription pipeline may execute local commands while processing media.

Mitigation: Review the scripts before installation and prefer a fixed version that removes shell=True, validates URLs and paths, preserves TLS verification, and uses private temporary directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/casperzinou/skills/reel-digest)
- [ClawHub publisher profile](https://clawhub.ai/user/casperzinou)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown digest with supporting transcript text, extracted frame references, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local video, audio, transcript, frame, and metadata files for analysis.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
