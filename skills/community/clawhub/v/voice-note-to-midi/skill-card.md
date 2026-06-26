## Description: <br>
Convert voice notes, humming, and melodic audio recordings to quantized MIDI files using ML-based pitch detection and intelligent post-processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DanBennettUK](https://clawhub.ai/user/DanBennettUK) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, musicians, and producers use this skill to turn clear melodic voice notes, humming, singing, or existing MIDI files into cleaner quantized MIDI for editing in a DAW. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer use brings ordinary third-party Python dependency risk. <br>
Mitigation: Review and, where appropriate, pin the Basic Pitch, librosa, soundfile, mido, and music21 dependencies before installing on sensitive machines. <br>
Risk: Manual setup may involve downloading a hum2midi script separately. <br>
Mitigation: Review the downloaded script before execution and prefer a trusted source or checked hash when operating in controlled environments. <br>
Risk: The optional PATH change can affect future terminal command lookup. <br>
Mitigation: Accept the PATH update only when desired, and remove the added shell profile export line to undo it. <br>


## Reference(s): <br>
- [Basic Pitch](https://github.com/spotify/basic-pitch) <br>
- [librosa HPSS](https://librosa.org/doc/latest/generated/librosa.decompose.hpss.html) <br>
- [Krumhansl-Kessler Key Profiles](https://rnhart.net/articles/key-finding/) <br>
- [Voice Note To Midi on ClawHub](https://clawhub.ai/DanBennettUK/voice-note-to-midi) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with inline shell commands and generated MIDI file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces MIDI conversion guidance and commands; command execution may create .mid files from supported audio or MIDI inputs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
