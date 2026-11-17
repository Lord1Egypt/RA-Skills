## Description:

Local text-to-speech using Piper voices via sherpa-onnx that generates offline Telegram-compatible voice replies without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stolot0mt0m](https://clawhub.ai/user/stolot0mt0m)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill when an agent should turn a text response into a local spoken reply, especially for Telegram voice-note workflows. It supports German and English voices and can auto-detect the language for basic voice selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer asks for root access and installs software under /opt.

Mitigation: Review the installer before use and run it only on machines where granting root access is acceptable.

Risk: The installer downloads third-party archives without verifying checksums or signatures.

Mitigation: Prefer or add a version that verifies published SHA-256 checksums or signatures before extraction and execution.

Risk: Downloaded binaries and models are extracted directly into privileged locations.

Mitigation: Download and extract as an unprivileged user in a staging directory, inspect the contents, then move approved files into place.

## Reference(s):

- [Voice Reply ClawHub Skill Page](https://clawhub.ai/stolot0mt0m/skills/voice-reply)
- [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx)
- [sherpa-onnx TTS Models](https://github.com/k2-fsa/sherpa-onnx/releases/tag/tts-models)
- [Piper](https://github.com/rhasspy/piper)
- [Piper Voice Samples](https://rhasspy.github.io/piper-samples/)
- [Thorsten Voice](https://github.com/thorstenMueller/Thorsten-Voice)

## Skill Output:

**Output Type(s):** [text, files]

**Output Format:** [Plain text control tag plus MEDIA path referencing an OGG Opus audio file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Telegram-compatible voice note output using local sherpa-onnx, Piper voice models, ffmpeg, and SHERPA_ONNX_DIR/PIPER_VOICES_DIR.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
