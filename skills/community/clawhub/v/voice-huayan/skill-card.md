## Description:

Local Chinese TTS playback on Windows using Piper zh_CN-huayan-medium with automatic fallback to System.Speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mecyalika](https://clawhub.ai/user/mecyalika)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill when they want an agent to read Chinese responses aloud through local Windows speaker playback in the huayan voice style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled setup scripts can install Python packages and download remote model assets from external services without verification.

Mitigation: Review scripts before installation, pin and verify dependencies and downloaded assets, and allow downloads only from approved sources.

Risk: The release package does not include the advertised playback script.

Mitigation: Confirm the expected Windows playback entry point is present and functional before deployment.

Risk: The bundled download script includes branches for model assets beyond the declared zh_CN-huayan-medium voice.

Mitigation: Limit execution to the declared huayan model path or remove unrelated download branches before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mecyalika/skills/voice-huayan)
- [Piper voices model assets](https://huggingface.co/rhasspy/piper-voices)
- [sherpa-onnx espeak-ng data release asset](https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/espeak-ng-data.tar.bz2)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline PowerShell command examples and playback status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Direct local audio playback with PLAYBACK_OK status on success]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
