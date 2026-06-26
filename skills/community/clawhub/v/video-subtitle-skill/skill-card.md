## Description: <br>
Generates subtitles for video or audio with SenseAudio ASR, including multilingual transcription, optional translation, speaker diarization, and video burn-in. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QWERTY0205](https://clawhub.ai/user/QWERTY0205) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill in Claude Code to turn local video or audio files into subtitle files, transcripts, optional translations, and optionally a subtitled video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send user media to SenseAudio for transcription. <br>
Mitigation: Require explicit user confirmation before remote upload and avoid confidential, regulated, or third-party media unless the user is allowed to send it to SenseAudio. <br>
Risk: The API-key check can expose the SenseAudio API key in terminal output. <br>
Mitigation: Use a redacted presence check for SENSEAUDIO_API_KEY instead of printing the secret value. <br>
Risk: Generated transcripts and subtitled videos may contain sensitive media content. <br>
Mitigation: Use a dedicated output folder and review retention or cleanup expectations before processing sensitive files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QWERTY0205/video-subtitle-skill) <br>
- [SenseAudio](https://senseaudio.cn) <br>
- [SenseAudio transcription API endpoint](https://api.senseaudio.cn/v1/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated agent artifacts include SRT, VTT, TXT, JSON, and optionally MP4 files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.10+, requests, ffmpeg, fonts-noto-cjk for CJK burn-in, and SENSEAUDIO_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
