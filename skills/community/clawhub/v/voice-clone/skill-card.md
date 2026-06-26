## Description: <br>
Guide users through SenseAudio platform voice cloning, then generate TTS with cloned `voice_id` values. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to prepare SenseAudio voice-cloning inputs, manage cloned voice IDs, and synthesize text-to-speech audio with a cloned voice after platform-side cloning is complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent needs access to a SenseAudio API key and may send synthesis text, voice IDs, and voice samples to SenseAudio. <br>
Mitigation: Use a dedicated API key with appropriate scope, avoid logging secrets, and confirm the user is comfortable sending the required data to SenseAudio. <br>
Risk: Voice cloning can misuse voices that the user does not own or have permission to clone. <br>
Mitigation: Proceed only with voices the user owns or is authorized to clone, and keep cloned voice IDs treated as user-specific operational identifiers. <br>
Risk: Unpinned Python dependencies can change behavior in controlled environments. <br>
Mitigation: Pin `requests` and `pydub` versions when deploying the skill in production or audited environments. <br>


## Reference(s): <br>
- [Voice Clone on ClawHub](https://clawhub.ai/scikkk/voice-clone) <br>
- [scikkk Publisher Profile](https://clawhub.ai/user/scikkk) <br>
- [SenseAudio Homepage](https://senseaudio.cn) <br>
- [SenseAudio Voice Clone Platform](https://senseaudio.cn/platform/voice-clone) <br>
- [SenseAudio API Key Platform](https://senseaudio.cn/platform/api-key) <br>
- [SenseAudio TTS API Endpoint](https://api.senseaudio.cn/v1/t2a_v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python helper code and optional JSON-style validation metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce synthesized audio files through SenseAudio API calls when the user supplies credentials and a cloned voice ID.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
