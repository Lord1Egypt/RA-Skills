## Description:

Text-to-speech conversion tool. Use when converting text to speech audio files (opus or mp3 format). Supports macOS native 'say' command and Google TTS (gTTS) service with ffmpeg audio conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyendt](https://clawhub.ai/user/wangyendt)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to convert text into Opus or MP3 speech audio through pywayne.tts, using macOS native speech where available or Google TTS with ffmpeg conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using gTTS sends converted text to Google's TTS service.

Mitigation: Use macOS native 'say' when appropriate, and avoid sending sensitive text to gTTS unless that service use is acceptable.

Risk: Audio conversion depends on ffmpeg and may prompt users to install or configure local tools.

Mitigation: Review installation prompts and install ffmpeg from trusted package managers or the official ffmpeg site before running conversions.

Risk: Generated audio files require write access to the selected output directory.

Mitigation: Choose an output directory with appropriate permissions and review file paths before writing audio.

## Reference(s):

- [ffmpeg](https://ffmpeg.org)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for creating Opus or MP3 audio files and checking required local tools.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
