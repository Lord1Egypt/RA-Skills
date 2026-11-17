## Description:

SenseAudio Voice CN provides text-to-speech and speech-to-text workflows with automatic language-based switching across SenseAudio and Edge TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cowboy231](https://clawhub.ai/user/cowboy231)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to synthesize speech from text, transcribe audio to text, and configure multilingual voice workflows for Chinese, English, and Japanese content.

### Deployment Geography for Use:

Global, with SenseAudio account setup and free-use requirements documented for users in mainland China.

## Known Risks and Mitigations:

Risk: Text or audio may be sent to SenseAudio or Microsoft Edge TTS cloud services.

Mitigation: Avoid sensitive recordings or text, confirm the service terms, and use the skill only where cloud speech processing is acceptable.

Risk: Generated audio and transcript files may be stored locally.

Mitigation: Review the local audio and transcript directories, apply appropriate file permissions, and remove retained files when no longer needed.

Risk: Setup installs Python dependencies and reads OpenClaw configuration paths for API credentials.

Mitigation: Install dependencies in a virtual environment with pinned versions, prefer a dedicated SENSE_API_KEY, and review configuration lookup before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cowboy231/skills/senseaudio-voice-cn)
- [SenseAudio Text-to-Speech API](https://senseaudio.cn/docs/text_to_speech_api)
- [SenseAudio Speech Recognition HTTP API](https://senseaudio.cn/docs/speech_recognition/http_api)
- [SenseAudio](https://senseaudio.cn)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated or transcribed text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local WAV or MP3 audio files and optional transcript files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
