## Description:

Convert text to speech using Microsoft Edge's TTS engine with customizable voices, direct playback, and automatic temporary file cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaov1976](https://clawhub.ai/user/zhaov1976)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use Voice to convert text into spoken audio, play generated or existing audio, list available voices, and clean up temporary audio files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell execution may run commands with user-controlled text or options.

Mitigation: Run only in a sandboxed environment and restrict or fix shell command construction before broader use.

Risk: Dependency installation can fetch and execute third-party package code.

Mitigation: Do not invoke the install action unless the dependency source is trusted and reviewed.

Risk: Audio output paths, playback paths, and cleanup behavior can affect local files.

Mitigation: Restrict allowed paths for generated files, playback, and cleanup before use outside a sandbox.

Risk: Text sent for speech generation may contain sensitive content.

Mitigation: Avoid using sensitive text with this skill unless data handling has been reviewed.

## Reference(s):

- [Voice Skill on ClawHub](https://clawhub.ai/zhaov1976/skills/voice)

## Skill Output:

**Output Type(s):** [text, files, shell commands, configuration]

**Output Format:** [JSON-style result objects with status text, MEDIA links, file paths, and voice lists.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary audio files and invoke a system audio player for playback.]

## Skill Version(s):

1.0.1 (source: server release metadata, created 2026-02-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
