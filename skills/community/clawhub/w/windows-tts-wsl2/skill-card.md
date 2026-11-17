## Description:

Windows TTS (WSL2) lets agents play spoken text through Windows 11 built-in System.Speech voices from WSL by invoking powershell.exe.

This skill is ready for commercial/non-commercial use.

## Publisher:

[547895019](https://clawhub.ai/user/547895019)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill when they need direct text-to-speech playback from WSL2 through the Windows default audio output, especially for Chinese voice prompts or environments where built-in TTS output is silent or unusable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted text, voice, rate, or volume values may execute unintended PowerShell commands on the Windows side.

Mitigation: Review inputs before use, use the skill only with trusted text and options, and prefer a safer implementation that passes values as data and validates numeric ranges before invoking PowerShell.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/547895019/skills/windows-tts-wsl2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill triggers direct Windows audio playback and does not return an audio file path.]

## Skill Version(s):

1.1.1 (source: server release evidence, created 2026-02-15T10:59:41Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
