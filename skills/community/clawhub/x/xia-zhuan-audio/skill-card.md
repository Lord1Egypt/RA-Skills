## Description:

Audio and video conversion, audio extraction, merging, splitting, compression, media information, and Whisper-based transcription using FFmpeg and faster-whisper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luis1213899](https://clawhub.ai/user/luis1213899)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to convert and process local audio or video files and to produce text, subtitle, or JSON transcriptions from media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FFmpeg commands use overwrite behavior and can replace local output files.

Mitigation: Run the skill only on trusted media and direct outputs to a reviewed working folder with backups for important files.

Risk: The merge flow uses a shared temporary file pattern that is unsafe on shared or multi-user systems.

Mitigation: Fix merge temporary-file handling before shared-system use, or run the skill only in an isolated single-user environment.

Risk: Whisper models may be downloaded at runtime unless already cached.

Mitigation: Use a virtual environment with pinned Python dependencies and pre-approved model cache locations or endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luis1213899/skills/xia-zhuan-audio)
- [Publisher profile](https://clawhub.ai/user/luis1213899)
- [Project homepage from metadata](https://github.com/luis12123899/xia-zhuan-audio)
- [FFmpeg](https://ffmpeg.org)
- [Hugging Face model source](https://huggingface.co)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples; generated media files and txt, srt, vtt, or json transcription files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FFmpeg, Python for transcription, and faster-whisper; Whisper models may be downloaded into the configured model directory.]

## Skill Version(s):

1.3.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
