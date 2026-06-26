## Description: <br>
Starts a persistent macOS voice assistant that listens through the microphone, transcribes speech with SenseAudio ASR, sends turns to the audioclaw agent, and responds with SenseAudio TTS or macOS say. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kikidouloveme79](https://clawhub.ai/user/kikidouloveme79) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AudioClaw/OpenClaw users use this skill to run hands-free, multi-turn voice conversations on macOS with SenseAudio ASR/TTS, wake and sleep phrases, optional voice preferences, and optional WeSpeaker speaker filtering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a long-running microphone assistant and sends captured speech to SenseAudio for transcription. <br>
Mitigation: Install and run it only when this microphone and network behavior is acceptable, review SenseAudio data handling terms, and stop the Terminal session when voice mode is no longer needed. <br>
Risk: The skill may store local preferences and optional WeSpeaker voiceprint profiles. <br>
Mitigation: Keep WeSpeaker disabled unless speaker filtering is required, and clear local profiles or state when they are no longer needed. <br>
Risk: The skill depends on a SenseAudio API key and local macOS microphone tooling. <br>
Mitigation: Use a scoped API key, keep local credentials protected, and run the startup self-check before relying on the assistant. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/kikidouloveme79/senseaudio-let-claw-talk) <br>
- [Runtime tuning guide](references/runtime_tuning.md) <br>
- [WeSpeaker user environment guide](references/wespeaker_user_setup.md) <br>
- [WeSpeaker project](https://github.com/wenet-e2e/wespeaker.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch a long-running local voice assistant process that uses microphone input, network API calls, local preference files, and optional local voiceprint state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
