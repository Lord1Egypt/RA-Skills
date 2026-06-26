## Description: <br>
Recommends suitable SenseAudio voice IDs for a user's scenario, emotion, or plan tier, with an optional TTS preview sample when a SenseAudio API key is available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and operators use this skill to select SenseAudio voices for narration, marketing, podcast, story, education, and emotion-driven voice scenarios. It can also provide shell commands for generating comparison MP3 previews when the user supplies SenseAudio credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Preview generation sends the preview text to the SenseAudio API and writes preview.json and MP3 files locally. <br>
Mitigation: Use the API key only when previews are needed, avoid confidential preview text, and delete generated preview files after use. <br>


## Reference(s): <br>
- [ClawHub Voice Picker release](https://clawhub.ai/scikkk/voice-picker) <br>
- [SenseAudio homepage](https://senseaudio.cn) <br>
- [SenseAudio API key page](https://senseaudio.cn/platform/api-key) <br>
- [SenseAudio TTS API endpoint](https://api.senseaudio.cn/v1/t2a_v2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown recommendations with optional bash commands that write preview JSON and MP3 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations usually include one to three voice options with voice ID, style, plan tier, and fit for the user's scenario.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
