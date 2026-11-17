## Description:

ElevenLabs text-to-speech with mac-style say UX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate local ElevenLabs speech audio from text, select voices and models, and tune pronunciation or delivery through sag command-line guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Speech text or other user-controlled input can be unsafe if interpolated directly into a shell string.

Mitigation: Pass speech text as a literal argument, preserve shell quoting, and review generated sag commands before execution.

Risk: ElevenLabs credentials can be exposed through command arguments, logs, shell history, or persisted files.

Mitigation: Keep credentials in environment variables such as ELEVENLABS_API_KEY, never print full or partial values, and do not write actual keys into scripts or env files.

Risk: Unbounded voice or model batches can create unexpected API usage and cost.

Mitigation: Proceed with small explicit batches only, and require confirmation before iterating over all voices, all models, or other open-ended sets.

Risk: Generated audio or credentials can be exfiltrated if piped to network-transmitting commands.

Mitigation: Keep generated audio as a local artifact and avoid piping sag output or credential values to tools such as curl, wget, nc, or scp.

## Reference(s):

- [Sag homepage](https://sag.sh)
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/sag-hardened)
- [Faberlens safety evaluation](https://faberlens.ai/explore/sag)
- [SAFETY.md](artifact/SAFETY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and local media file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local audio files such as MP3 artifacts through sag.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
