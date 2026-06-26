## Description: <br>
Generate synchronized SRT, VTT, and ASS subtitles from video audio with precise timestamps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video creators use this skill to extract audio from video, transcribe it with SenseAudio, and generate synchronized caption files or burned-in subtitles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video audio is sent to SenseAudio for transcription, which may expose confidential or regulated recordings. <br>
Mitigation: Use only recordings permitted by policy, avoid confidential content unless approved, and keep the SenseAudio API key private. <br>
Risk: Generated subtitle or video outputs can overwrite existing files if filenames are reused. <br>
Mitigation: Choose fresh output filenames and review generated subtitles before publishing or embedding them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scikkk/subtitle) <br>
- [SenseAudio homepage](https://senseaudio.cn) <br>
- [SenseAudio speech recognition API docs](https://senseaudio.cn/docs/speech_recognition) <br>
- [SenseAudio API key page](https://senseaudio.cn/platform/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with Python and shell code blocks; generated artifacts may be SRT, VTT, ASS, JSON, or video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY and ffmpeg; sends extracted audio to SenseAudio for transcription.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
