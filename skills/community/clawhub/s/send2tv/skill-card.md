## Description: <br>
Pushes text messages, images, audio, or TTS playback to Huawei Smart Screen and other DLNA-compatible TVs via DLNA/UPnP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanshen-lec](https://clawhub.ai/user/seanshen-lec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to send text, photos, audio files, or generated speech from an agent environment to a DLNA-compatible television on a trusted local network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill briefly exposes selected media through a local HTTP server on the LAN. <br>
Mitigation: Use only on trusted LANs and avoid sending sensitive text, images, or audio. <br>
Risk: The skill can stop another local service that is using TCP port 8082. <br>
Mitigation: Check for services using port 8082 before running and change the port or stop conflicting services intentionally. <br>
Risk: TTS mode depends on a separate edge-tts skill. <br>
Mitigation: Review the edge-tts skill before use and avoid sending sensitive text to TTS mode. <br>


## Reference(s): <br>
- [Send2tv ClawHub page](https://clawhub.ai/seanshen-lec/send2tv) <br>
- [Microsoft Speech voice gallery](https://speech.microsoft.com/portal/voicegallery) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text, Audio, Guidance] <br>
**Output Format:** [Command-line execution that creates temporary JPEG or MP3 files, serves them over local HTTP, and sends DLNA/UPnP playback commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted LAN, configured TV and local IP addresses, Pillow, optional ffmpeg for audio conversion, and the separate edge-tts skill for TTS mode.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
