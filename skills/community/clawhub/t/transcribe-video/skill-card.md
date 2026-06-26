## Description: <br>
Extracts transcript text or embedded subtitles from local video files, using ffmpeg or ffprobe first and an OpenAI or Azure-compatible transcription API when subtitles are unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feiskyer](https://clawhub.ai/user/feiskyer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to produce transcripts from local video files, preferring embedded subtitle extraction and falling back to API-based speech recognition when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Videos without embedded subtitles may have audio sent to the configured OpenAI or Azure-compatible transcription provider. <br>
Mitigation: Use API transcription only for videos approved for that provider, protect ~/.transcribe_video.env with restrictive permissions, and verify OPENAI_API_BASE points to a trusted endpoint. <br>
Risk: The helper may reuse and delete a same-named .wav file beside the source video. <br>
Mitigation: Check for an existing .wav file with the same basename before running API transcription and preserve or rename it if needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/feiskyer/transcribe-video) <br>
- [Publisher profile](https://clawhub.ai/user/feiskyer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated transcript text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a .txt transcript beside the source video and may create, upload, and delete a same-named .wav audio file when API transcription is used; protect API credentials and verify the configured transcription endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
