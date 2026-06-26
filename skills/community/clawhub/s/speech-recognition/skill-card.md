## Description: <br>
Transcribes user-supplied voice messages and audio files with SiliconFlow SenseVoice, including common formats such as OGG, MP3, WAV, M4A, and FLAC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[demo112](https://clawhub.ai/user/demo112) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to convert audio or voice-message inputs into text through the SiliconFlow transcription API. It is suited for workflows where users ask to transcribe uploaded audio and are comfortable sending that audio to SiliconFlow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio files are sent to SiliconFlow for transcription. <br>
Mitigation: Only transcribe audio the user is comfortable sending to SiliconFlow, especially voice messages or meeting recordings. <br>
Risk: The transcription workflow requires a SiliconFlow API key. <br>
Mitigation: Use a dedicated or revocable API key such as SILICONFLOW_API_KEY. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/demo112/speech-recognition) <br>
- [SiliconFlow audio transcription endpoint](https://api.siliconflow.cn/v1/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python, bash, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SiliconFlow API key and may use FFmpeg conversion before transcription.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
