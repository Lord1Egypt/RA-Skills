## Description: <br>
Transcribe YouTube videos by extracting captions first and falling back to local Whisper transcription when captions are unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iml885203](https://clawhub.ai/user/iml885203) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill when a YouTube link needs to be turned into transcript text for reading, summarization, note-taking, or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: yt-dlp contacts YouTube for user-provided video links. <br>
Mitigation: Use the skill only with links the user intends to process and understands will be fetched from YouTube. <br>
Risk: When captions are unavailable, the skill temporarily downloads audio for local Whisper transcription. <br>
Mitigation: Run Whisper fallback only in an environment appropriate for the video's content and dependencies, and rely on the temporary-file workflow to avoid persistent audio storage. <br>
Risk: The --output option writes transcript content to a user-specified path. <br>
Mitigation: Check the output path before saving transcripts. <br>


## Reference(s): <br>
- [YouTube Transcribe on ClawHub](https://clawhub.ai/iml885203/youtube-transcribe) <br>
- [Publisher profile](https://clawhub.ai/user/iml885203) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcript by default, with optional JSON, SRT, VTT, or saved file output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses yt-dlp for captions and temporary audio retrieval; Whisper fallback can use MLX Whisper, faster-whisper, or OpenAI Whisper depending on local availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
