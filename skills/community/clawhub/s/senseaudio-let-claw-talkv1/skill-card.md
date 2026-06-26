## Description: <br>
Runs a hands-free desktop voice assistant on macOS and Windows that listens through the microphone, transcribes speech with SenseAudio ASR, sends text to AudioClaw, and reads responses with SenseAudio TTS or system speech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kikidouloveme79](https://clawhub.ai/user/kikidouloveme79) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to launch and tune a hands-free local voice assistant for multi-turn voice conversations, continuous voice control, and desktop assistant prototypes on macOS or Windows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start a long-running microphone assistant and send speech and reply text to SenseAudio cloud APIs. <br>
Mitigation: Install only when that behavior is acceptable, review the wake phrase, and disable the assistant when it is not in active use. <br>
Risk: The skill keeps local state, logs, generated reply audio, preferences, credentials, and optional voice profiles in the user's workspace. <br>
Mitigation: Protect the SenseAudio credential file and periodically clear workspace logs, preferences, generated reply audio, and unused voice profiles. <br>
Risk: Optional WeSpeaker voiceprint verification can run as a local background service. <br>
Mitigation: Enable WeSpeaker only when needed and keep its service bound to 127.0.0.1. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kikidouloveme79/senseaudio-let-claw-talkv1) <br>
- [Runtime Tuning](artifact/references/runtime_tuning.md) <br>
- [WeSpeaker User Environment Guide](artifact/references/wespeaker_user_setup.md) <br>
- [WeSpeaker repository](https://github.com/wenet-e2e/wespeaker.git) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch a long-running local microphone assistant process and write user-level state, logs, generated reply audio, preferences, and optional voice profiles.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
