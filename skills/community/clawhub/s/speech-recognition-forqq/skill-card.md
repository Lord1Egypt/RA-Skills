## Description:

Converts QQ voice messages and AMR/SILK audio files to text using pysilk decoding and faster-whisper transcription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yvanboyang](https://clawhub.ai/user/yvanboyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add speech-to-text handling for QQ voice messages and AMR/SILK audio files, including dependency setup, model download, and a simple Python transcription call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing unpinned packages and downloading the faster-whisper model can introduce dependency, supply-chain, or policy review risk.

Mitigation: Use a dedicated virtual environment, pin reviewed package versions, and confirm HuggingFace model downloads are allowed by network and data policies before running commands.

Risk: The skill processes user-provided voice files that may contain sensitive spoken content.

Mitigation: Handle audio files according to the user's data handling requirements and avoid sending protected audio to environments that are not approved for that data.

Risk: The provided setup instructions are partly Chinese-language and environment-specific.

Mitigation: Translate and review the instructions before execution, and adjust paths and environment names to the target system.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yvanboyang/skills/speech-recognition-forqq)
- [Systran faster-whisper-base Model](https://huggingface.co/Systran/faster-whisper-base)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers local audio decoding, WAV conversion, faster-whisper transcription, dependency installation, and model download requirements.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
