## Description:

Windows local text-to-speech skill that reads visible agent replies through a small local playback window with queued speech, sentence splitting, and speed and volume controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[512548510](https://clawhub.ai/user/512548510)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Windows users use this skill to have agent replies read aloud locally while keeping the same reply visible in chat. It is intended for local Windows text-to-speech workflows that need queued playback and adjustable voice speed and volume.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local Windows helper accepts unauthenticated same-session messages while it is running.

Mitigation: Run it only in a trusted local session, close it when TTS is not needed, and avoid sending secrets while TTS mode is enabled.

Risk: The helper invokes PowerShell for speech playback.

Mitigation: Review the bundled scripts before installation, pin pywin32, and run the skill in a limited environment.

Risk: A debug test script is included with the artifact.

Mitigation: Ignore or remove the debug test script unless it is needed for local troubleshooting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/512548510/skills/tts-winmsg-free)
- [Project homepage](https://github.com/512548510/openclaw-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and local configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-visible replies that may also be forwarded to a local Windows TTS helper when TTS mode is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
