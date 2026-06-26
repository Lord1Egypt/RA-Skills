## Description: <br>
Quick TTS turns user-provided text into an MP3 with SenseAudio, selecting voices from natural-language requests and adding pacing breaks for longer text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to synthesize text into MP3 audio through SenseAudio without manually assembling API calls or voice IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided text to the external SenseAudio API. <br>
Mitigation: Use it only when SenseAudio handling is acceptable, and avoid synthesizing secrets, regulated data, or private text. <br>
Risk: The shell example inserts text into a JSON payload inside a curl command. <br>
Mitigation: Build the JSON payload with a safe JSON encoder before execution instead of directly substituting user text into shell-quoted JSON. <br>
Risk: The skill requires a SenseAudio API key. <br>
Mitigation: Use a scoped, revocable API key and rotate or revoke it if exposure is suspected. <br>


## Reference(s): <br>
- [Quick TTS on ClawHub](https://clawhub.ai/scikkk/quick-tts) <br>
- [SenseAudio](https://senseaudio.cn) <br>
- [SenseAudio API Key](https://senseaudio.cn/platform/api-key) <br>
- [SenseAudio Text-to-Audio API](https://api.senseaudio.cn/v1/t2a_v2) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Markdown, Guidance] <br>
**Output Format:** [MP3 audio file with Markdown status summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports file path, voice used, audio duration, and character count when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
