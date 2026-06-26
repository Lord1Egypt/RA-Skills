## Description: <br>
Replace video audio with TTS voice while preserving original timing. Includes subtitle generation from video using Whisper. Uses ElevenLabs or Edge TTS, aligns each audio segment to original timestamp, adjusts speed (0.85-1.15x), and inserts silence gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[synthere](https://clawhub.ai/user/synthere) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and media automation users can replace a video's original audio with TTS narration aligned to subtitle timing, or generate subtitles from a source video before dubbing. Typical uses include AI voice-over, subtitle-to-speech conversion, and multilingual video versions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media files and subtitle text may include copyrighted, private, or sensitive content, and ElevenLabs TTS sends transcript text to a cloud provider. <br>
Mitigation: Use the skill only with media and subtitles the user is allowed to process, avoid cloud TTS for confidential transcripts unless provider terms are acceptable, or choose the local/free Edge TTS path when appropriate. <br>
Risk: The workflow writes generated subtitles, temporary audio, and final video files, so careless paths can overwrite desired outputs. <br>
Mitigation: Choose a fresh output filename and review the command arguments before running the replacement workflow. <br>
Risk: The ElevenLabs path requires an API key and third-party dependency installation. <br>
Mitigation: Use a dedicated revocable ElevenLabs key and install Python dependencies in a virtual environment rather than with system-wide privileged pip installs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/synthere/video-audio-replace) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with command examples and generated media file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces SRT subtitle files and dubbed MP4 video files when executed with local media, ffmpeg, and a selected TTS engine.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
