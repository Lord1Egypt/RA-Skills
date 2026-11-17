## Description:

Use when the user wants to open, stop, configure, debug, or package the SenseAudio floating audio assistant in AudioClaw, including system-audio subtitles, bilingual ASR/translation, recent-project organization, copied-text TTS, music generation, or macOS audio routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kkzz1225](https://clawhub.ai/user/kkzz1225)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and AudioClaw users use this skill to run and maintain a macOS floating audio assistant for system-audio subtitles, bilingual ASR/translation, copied-text TTS, music generation, and transcript organization. It also provides setup, status, stop, diagnostics, and troubleshooting commands for the local audio route and SenseAudio integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live audio, transcripts, generated media metadata, and workspace state that may contain sensitive information.

Mitigation: Use it only in trusted workspaces, review what is captured or persisted, and keep workspace state out of shared archives or backups unless secrets and sensitive transcripts are redacted.

Risk: SenseAudio credentials are required for ASR, translation, TTS, and music features.

Mitigation: Provide credentials through the AudioClaw runtime, do not paste keys into chat or committed files, and rely on the included smoke script only for presence checks unless a live quota-consuming test is intended.

Risk: Network calls should continue to target the intended SenseAudio service endpoints.

Mitigation: Before live capture, verify the configured ASR endpoint remains the official SenseAudio URL and review local configuration before running.

Risk: The dependency setup is not described as patched or hash-pinned in the server security guidance.

Mitigation: Prefer a patched and hash-pinned dependency installation process before deployment in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kkzz1225/skills/senseaudio-floating-audio-assistant-v2)
- [Quickstart](references/quickstart.md)
- [Operator Notes](references/operator_notes.md)
- [SenseAudio Integration](references/senseaudio_integration.md)
- [Troubleshooting](references/troubleshooting.md)
- [Runtime README](runtime/realtime_interpreter/README.md)
- [Cross-platform Overlay README](runtime/realtime_interpreter/cross_platform_overlay/README.md)
- [SenseAudio TTS API endpoint](https://api.senseaudio.cn/v1/t2a_v2)
- [SenseAudio music generation API endpoint](https://api.senseaudio.cn/v1/music/song/create)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration notes, and runnable local scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance and commands for a macOS AudioClaw/SenseAudio runtime; the artifact bundles scripts, presets, and source files but no local credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
