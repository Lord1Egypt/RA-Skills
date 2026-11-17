## Description:

Send native voice messages to WeCom using Windows TTS and convert text to speech as a native voice message rather than an audio file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanqisyx](https://clawhub.ai/user/fanqisyx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate WeCom voice messages from text on Windows systems. It is intended for workflows that need text converted to speech with Windows System.Speech, converted to AMR, and sent through WeCom using OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated audio is sent externally through WeCom and the current behavior can use an under-disclosed default recipient.

Mitigation: Require an explicit recipient and clearly confirm the destination before sending.

Risk: The authoritative security evidence reports command-injection flaws in message text and recipient handling.

Mitigation: Use argument-safe process APIs and validate or escape untrusted text and recipient values before execution.

Risk: Temporary speech and media files may remain on disk.

Mitigation: Remove temporary files after sending or store them in a secured location with clear retention behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fanqisyx/skills/wecom-voice)
- [Publisher profile](https://clawhub.ai/user/fanqisyx)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration instructions]

**Output Format:** [Node.js CLI execution that creates WAV and AMR voice media and sends a WeCom voice message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Windows System.Speech, FFmpeg, OpenClaw, and a WeCom target recipient.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
