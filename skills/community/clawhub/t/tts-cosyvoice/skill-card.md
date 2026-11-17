## Description:

Text-to-Speech via Edge TTS (Microsoft Azure voices). Free, no API key needed, supports 100+ voices in 50+ languages including Chinese and English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert text or text files into speech through Microsoft Edge TTS voices, with options for voice, rate, pitch, volume, language-filtered voice listing, and optional SRT subtitle generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send submitted text to Microsoft-operated cloud TTS infrastructure.

Mitigation: Do not submit sensitive text unless that data transfer is approved; use an offline TTS path for confidential content.

Risk: The release includes code-loading and setup patterns that could execute unreviewed third-party Python code.

Mitigation: Review before installing, use a dedicated virtual environment with pinned dependencies, remove the hard-coded /home/vincent sys.path override, and avoid trust_remote_code examples unless pinned and sandboxed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vincentlau2046-sudo/skills/tts-cosyvoice)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with bash commands; generated outputs are MP3 audio files and optional SRT subtitle files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the edge-tts Python package, and an internet connection to reach Microsoft-operated TTS infrastructure.]

## Skill Version(s):

1.2.0 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
