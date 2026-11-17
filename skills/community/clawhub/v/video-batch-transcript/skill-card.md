## Description:

视频批量转录 uses yt-dlp and faster-whisper to batch download authorized video or audio sources, transcribe speech with optional CUDA acceleration, correct terminology, and generate structured notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and analysts use this skill to process authorized videos, playlists, channels, and course media into transcripts, structured notes, and collection summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser session cookies may be used for authenticated media sites.

Mitigation: Avoid --cookies-from-browser unless needed, prefer site-scoped exported cookie files, and store cookie files outside shared folders.

Risk: Remote media metadata may influence output paths, and evidence notes a path-building bug that can write outside the chosen output directory.

Mitigation: Fix path sanitization before processing untrusted URLs and run the skill with a dedicated output directory.

Risk: The skill downloads and transcribes external media.

Mitigation: Process only content the user is authorized to download and review generated transcripts and notes before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/skills/video-batch-transcript)
- [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)
- [Usage examples](artifact/examples/usage_examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown and text files with JSON metadata, plus shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes transcripts, notes, summaries, audio files, and metadata under the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
