## Description: <br>
Generate SenseAudio TTS narration tracks for videos, including timestamped segments, style variants, and editor-ready voiceover exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Video creators, developers, and production teams use this skill to generate timed SenseAudio narration, alternate voice takes, and editor-ready voiceover assets for video workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends narration text to the SenseAudio API, so confidential scripts may be exposed to a third-party service. <br>
Mitigation: Use only content approved for SenseAudio processing and avoid sending confidential scripts unless provider processing is acceptable. <br>
Risk: The SenseAudio API key can grant access to paid or production services if exposed. <br>
Mitigation: Use SENSEAUDIO_API_KEY from the environment, prefer scoped or dedicated keys when available, and do not place credentials in query strings, logs, or saved examples. <br>
Risk: Generated narration files and returned trace IDs may contain sensitive production data. <br>
Mitigation: Handle generated assets and trace IDs as sensitive data and apply normal project storage and sharing controls. <br>
Risk: The workflow depends on SenseAudio, ffmpeg, and Python packages. <br>
Mitigation: Install only when the SenseAudio service and declared Python packages are trusted for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/scikkk/video-narrator) <br>
- [SenseAudio](https://senseaudio.cn) <br>
- [SenseAudio API Key Page](https://senseaudio.cn/platform/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python snippets and JSON API request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include timestamped segment metadata, SenseAudio TTS settings, and local assembly steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
