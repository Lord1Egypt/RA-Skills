## Description:

Build and use whisper.cpp for local speech-to-text workflows, with optional cloud fallback when local transcription is not practical.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuxuclassmate](https://clawhub.ai/user/xuxuclassmate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and operators use this skill to build whisper.cpp, prepare audio, run local speech-to-text transcription, and choose an approved cloud fallback when local transcription is not practical.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Building third-party code from a moving upstream branch can change the behavior or trust boundary of local transcription over time.

Mitigation: Pin whisper.cpp to a known release or commit before building and review updates before adopting them.

Risk: Downloaded transcription models may be tampered with or may not match the intended source.

Mitigation: Download models only from official sources and verify hashes when available.

Risk: Using a fixed temporary audio path can expose private audio or leave sensitive files behind.

Mitigation: Use a unique private temporary file for each transcription and remove it after use.

Risk: Cloud transcription fallback sends audio outside the local machine.

Mitigation: Use cloud fallback only with user acceptance and an approved speech API.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xuxuclassmate/skills/whisper-voice-transcription)
- [whisper.cpp](https://github.com/ggerganov/whisper.cpp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.1.1 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
