## Description:

Synthesize speech by cloning a user's voice from a reference audio sample and reading generated text aloud in that cloned voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conanwhf](https://clawhub.ai/user/conanwhf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn an agent's text response into cloned-voice speech from a user-provided reference audio file. It is suited for voice-message replies, read-aloud requests, and voice-mode conversations where the speaker has authorized use of the reference voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs local voice cloning and handles voice samples as biometric data.

Mitigation: Use only with the speaker's permission and store or route reference audio according to the deployment's privacy requirements.

Risk: Installation can download large model weights and unpinned third-party code.

Mitigation: Review the installation scripts and dependency sources before running them in a production or shared environment.

Risk: The skill starts a background local service for synthesis.

Mitigation: Keep the service bound to 127.0.0.1 and avoid untrusted .env configuration files.

Risk: Cleanup scripts remove virtual environments, registrations, and optionally downloaded model weights.

Mitigation: Review uninstall behavior before running cleanup commands, especially with purge options.

## Reference(s):

- [Architecture](references/architecture.md)
- [ClawHub Skill Page](https://clawhub.ai/conanwhf/skills/voice-clone-bot)
- [ChatTTS](https://github.com/2noise/ChatTTS.git)
- [CosyVoice](https://github.com/FunAudioLLM/CosyVoice.git)
- [OpenVoice](https://github.com/myshell-ai/OpenVoice.git)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and generated audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a single absolute path to a generated .ogg file for MEDIA attachment.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
