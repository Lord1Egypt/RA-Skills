## Description: <br>
Transcribe audio and video files using a Whisper-compatible API endpoint, including automatic audio extraction from video files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djismgaming](https://clawhub.ai/user/djismgaming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to turn audio or video recordings into transcripts, captions, subtitles, or structured transcription output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio and video recordings may contain sensitive speech and are uploaded to a hardcoded plain-HTTP local-network endpoint. <br>
Mitigation: Use only with a trusted endpoint you control, avoid sensitive recordings, and prefer a secured configurable HTTPS endpoint with known retention and logging behavior. <br>
Risk: The endpoint address is fixed to `192.168.0.11:8080`, which may fail or route media to an unintended local service in other environments. <br>
Mitigation: Confirm the endpoint before use and update the implementation to require explicit endpoint configuration before uploading media. <br>


## Reference(s): <br>
- [Transcription Guide](references/transcription_guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/djismgaming/transcription) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text transcripts, JSON transcription responses, SRT subtitles, VTT captions, or Markdown guidance with shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May extract audio from video files with ffmpeg before sending media to the configured Whisper-compatible endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
