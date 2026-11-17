## Description:

Convert voice notes, humming, and melodic audio recordings to quantized MIDI files using ML-based pitch detection and intelligent post-processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danbennettuk](https://clawhub.ai/user/danbennettuk)

### License/Terms of Use:

MIT

## Use Case:

Developers, musicians, and producers use this skill to convert pitched voice memos, humming, singing, or existing MIDI into cleaner quantized MIDI suitable for DAW workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is incomplete without the hum2midi executable.

Mitigation: Confirm the executable source before installation and document or package a pinned, auditable version.

Risk: Installation guidance may lead users to run a mutable remote script.

Mitigation: Audit and pin external code and Python dependencies before use.

Risk: Adding the install directory to PATH creates a persistent user-level shell change.

Mitigation: Only add the directory to PATH when persistent command access is intended.

## Reference(s):

- [Basic Pitch](https://github.com/spotify/basic-pitch)
- [librosa HPSS](https://librosa.org/doc/latest/generated/librosa.decompose.hpss.html)
- [Krumhansl-Kessler Key Profiles](https://rnhart.net/articles/key-finding/)
- [ClawHub skill page](https://clawhub.ai/danbennettuk/skills/voice-note-to-midi)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [markdown with inline shell commands and option tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local audio-to-MIDI setup and use; generated workflow output is a standard MIDI file.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
