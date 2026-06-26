## Description: <br>
SenseAudio Text-to-Speech (TTS) API for converting text to natural speech with synchronous and SSE streaming modes, multiple voices, emotion control, speed, pitch, volume adjustment, and Chinese/English support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to integrate SenseAudio text-to-speech synthesis, including authentication, request parameters, synchronous responses, SSE streaming, and curl or Python examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis is sent to SenseAudio using an API key. <br>
Mitigation: Review SenseAudio's terms before use and avoid submitting secrets, regulated data, or private content unless approved for that environment. <br>
Risk: The examples can write response JSON and generated audio files to local paths. <br>
Mitigation: Choose output filenames deliberately and review generated files before sharing or deploying them. <br>


## Reference(s): <br>
- [SenseAudio Text-to-Speech documentation](https://senseaudio.cn/docs/text_to_speech_introduction) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with JSON, bash, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY and may produce local response JSON or audio files when examples are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
