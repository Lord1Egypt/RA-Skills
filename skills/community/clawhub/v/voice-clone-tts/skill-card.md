## Description: <br>
Voice Clone TTS guides agents through cloning a voice from audio samples and generating speech with MiniMax, ElevenLabs, Fish Audio, Azure TTS, or OpenAI TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OliviaPp8](https://clawhub.ai/user/OliviaPp8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to clone consented voices or synthesize narration for audio and video workflows, including batch generation from scene scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice samples, scripts, provider API keys, and voice IDs may be sensitive and may be sent to the selected TTS provider. <br>
Mitigation: Use only providers whose retention and deletion policies are acceptable, protect API keys and voice IDs, and avoid uploading sensitive audio unless that sharing is intended. <br>
Risk: Voice cloning can enable impersonation or misleading public content when used without permission. <br>
Mitigation: Use only voices the operator owns or has explicit consent to clone, and avoid deceptive or unauthorized impersonation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/OliviaPp8/voice-clone-tts) <br>
- [Backend setup guide](references/backend-setup.md) <br>
- [ElevenLabs API reference](https://docs.elevenlabs.io/api-reference) <br>
- [Fish Audio documentation](https://docs.fish.audio/) <br>
- [OpenAI speech API example](https://api.openai.com/v1/audio/speech) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML and JSON examples plus bash API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Voice cloning returns voice IDs; speech synthesis returns audio file paths and batch audio lists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
