## Description: <br>
Create animated talking-circle videos, similar to Telegram-style round video messages, from avatar frame images and audio, with audio-to-video and text-to-video workflows using ElevenLabs or SaluteSpeech TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Rai220](https://clawhub.ai/user/Rai220) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, creators, and developers use this skill to generate circular talking-avatar videos from four prepared avatar frames and either an existing audio file or synthesized speech. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SaluteSpeech mode disables HTTPS certificate verification while handling credentials. <br>
Mitigation: Avoid SaluteSpeech mode until TLS verification is fixed; prefer audio-to-video mode or ElevenLabs mode in a trusted environment. <br>
Risk: Scripts install unpinned Python packages at runtime. <br>
Mitigation: Review and install pinned dependencies in a controlled environment before running the skill. <br>
Risk: Text submitted to cloud TTS providers may contain private or regulated content. <br>
Mitigation: Use existing audio or a trusted local TTS path for sensitive content, or confirm the selected provider's data handling policies before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Rai220/talking-circle) <br>
- [ElevenLabs](https://elevenlabs.io) <br>
- [ElevenLabs Voice Library](https://elevenlabs.io/voice-library) <br>
- [SaluteSpeech](https://developers.sber.ru/portal/products/smartspeech) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [MP4 video files, generated avatar frame files, and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.9+, ffmpeg, four matching square PNG avatar frames, and optional TTS credentials for cloud speech synthesis.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
