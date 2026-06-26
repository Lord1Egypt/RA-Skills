## Description: <br>
Text-to-speech conversion tool. Use when converting text to speech audio files (opus or mp3 format). Supports macOS native 'say' command and Google TTS (gTTS) service with ffmpeg audio conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyendt](https://clawhub.ai/user/wangyendt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to convert text into Opus or MP3 speech audio, using macOS native speech output when available or Google TTS when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text sent through gTTS may be processed by a third-party service. <br>
Mitigation: Prefer the local macOS say path for private text when available, and do not send secrets, credentials, regulated data, or confidential content through gTTS unless third-party processing is acceptable. <br>
Risk: Audio conversion depends on local ffmpeg and Python package installations. <br>
Mitigation: Install ffmpeg, gtts, and pywayne dependencies only from trusted sources and verify they are available before relying on the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyendt/tts-2) <br>
- [FFmpeg](https://ffmpeg.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands] <br>
**Output Format:** [Markdown with Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for generating Opus or MP3 audio files; actual audio output depends on ffmpeg, platform support, and gTTS availability.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
