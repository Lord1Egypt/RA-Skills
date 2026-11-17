## Description:

ElevenLabs text-to-speech with mac-style say UX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy27725](https://clawhub.ai/user/andy27725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn text responses into local ElevenLabs speech audio with configurable voices, model choices, pronunciation guidance, and playback-oriented CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party Homebrew tap and the sag CLI.

Mitigation: Install only if the publisher and Homebrew tap are trusted for the deployment environment.

Risk: Text provided for speech generation may be sent to ElevenLabs through the configured API key.

Mitigation: Avoid sensitive text unless that use is allowed by the applicable ElevenLabs and organizational usage policies.

Risk: The documented chat voice example writes to /tmp/voice-reply.mp3 and can overwrite an existing file at that path.

Mitigation: Use a deliberate output path when existing audio should be preserved.

## Reference(s):

- [sag homepage](https://sag.sh)
- [ClawHub skill page](https://clawhub.ai/andy27725/skills/sag-andy27725)
- [Publisher profile](https://clawhub.ai/user/andy27725)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown with inline bash code blocks and generated audio file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a sag CLI installation and an ElevenLabs API key; examples may write MP3 output to a local /tmp path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
