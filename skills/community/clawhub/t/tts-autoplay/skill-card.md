## Description:

Auto-plays TTS voice files for OpenClaw Windows Webchat when wake-word or tagged-mode conditions request audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzjhz](https://clawhub.ai/user/wangzjhz)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and developers use this skill to configure conditional text-to-speech playback in Windows Webchat, so responses remain text-only by default and play audio when a wake word or tagged TTS response requests it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and runtime instructions reference PowerShell scripts that are not present in the provided artifact evidence.

Mitigation: Verify the actual package scripts from the trusted package source before running installation or autoplay commands.

Risk: Playback controls are inconsistent between tagged, always-on, and wake-word modes, which can cause unexpected audio output.

Mitigation: Review the OpenClaw TTS mode and wake-word settings, test both text-only and voice-triggered flows, and avoid elevated PowerShell sessions.

Risk: Unexpected TTS playback can expose private assistant replies to people nearby.

Mitigation: Use tagged mode for daily use, choose narrow wake words, and confirm voice and language settings before enabling autoplay.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangzjhz/skills/tts-autoplay)
- [README](artifact/README.md)
- [Wake Word Design](artifact/WAKE-WORD-DESIGN.md)
- [Wake Word Summary](artifact/WAKE-WORD-SUMMARY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON and PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets Windows/OpenClaw TTS workflows and PowerShell-based setup.]

## Skill Version(s):

2.0.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
