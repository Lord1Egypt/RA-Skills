## Description: <br>
Synthesize speech by cloning a user's voice from a reference audio sample, then reading generated text aloud in that cloned voice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[conanwhf](https://clawhub.ai/user/conanwhf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to turn an agent's text reply into cloned-voice speech from a local reference audio sample. It is intended for voice-message replies, read-aloud flows, and voice-mode conversations when the speaker has consented to voice cloning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive voice samples and can generate cloned speech. <br>
Mitigation: Use only with explicit speaker consent, keep reference audio local, and avoid deploying it in workflows where generated speech could be mistaken for unapproved human speech. <br>
Risk: Installation and runtime behavior can download and execute third-party model code, register the skill globally, run a background daemon, and store large model files. <br>
Mitigation: Review and pin dependencies before production use, install in an isolated environment, and monitor the daemon and model cache locations. <br>
Risk: The local API and output directory options can write generated files to disk and could expose voice generation if misconfigured. <br>
Mitigation: Bind the service to localhost, avoid passing arbitrary output directories, and restrict filesystem permissions for generated audio. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/conanwhf/voice-clone-bot) <br>
- [Architecture reference](references/architecture.md) <br>
- [ChatTTS engine source](https://github.com/2noise/ChatTTS) <br>
- [CosyVoice engine source](https://github.com/FunAudioLLM/CosyVoice) <br>
- [OpenVoice engine source](https://github.com/myshell-ai/OpenVoice) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Absolute .ogg audio file path and MEDIA:<path> attachment marker] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local TTS service, accepts text plus an optional reference audio path, and writes generated audio files to disk.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
