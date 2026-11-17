## Description:

Intelligent speech-to-text using local OpenAI Whisper with smart model selection for transcribing audio files without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[08jacky04](https://clawhub.ai/user/08jacky04)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent users use this skill to transcribe local audio files, voice messages, meetings, and multilingual speech into text. It can choose a Whisper model automatically based on audio duration and complexity, or use a caller-selected model and language hint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence marks the release suspicious because installation and runtime behavior are broader and less safely scoped than the privacy/offline wording suggests.

Mitigation: Review the skill before deployment, use an isolated virtual environment, pin reviewed dependency versions, and avoid the bundled install fallback on sensitive or shared systems.

Risk: The skill depends on external package and model downloads during setup or first use.

Mitigation: Install only from reviewed package sources and prefetch or approve model artifacts before use in controlled environments.

Risk: Runtime imports can use a /tmp/whisper-venv site-packages path if present.

Mitigation: Remove or review the /tmp/whisper-venv sys.path behavior before use on sensitive machines.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/08jacky04/skills/smart-voice-recognition)
- [Artifact README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [SoundFile Documentation](https://python-soundfile.readthedocs.io/)
- [PyTorch](https://pytorch.org/)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Plain text transcript, optionally saved as a text file; usage guidance is Markdown with shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include segment-level timestamps on stderr when requested.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
